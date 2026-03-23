from __future__ import annotations

from dataclasses import asdict
from typing import Any

import requests

from .types import InstanceData, InstanceMetadata, SubmitResult


class TSPClient:
    def __init__(self, base_url: str, timeout_s: float = 20.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def list_instances(self) -> dict[str, InstanceMetadata]:
        data = self._get_json("/instances")
        return {
            instance_id: InstanceMetadata(
                name=meta["name"],
                n_cities=int(meta["n_cities"]),
            )
            for instance_id, meta in data.items()
        }

    def get_instance(self, instance_id: str) -> InstanceData:
        data = self._get_json(f"/instances/{instance_id}")
        cities = [self._parse_city(raw_city) for raw_city in data["cities"]]
        return InstanceData(
            instance_id=data["instance_id"],
            name=data["name"],
            cities=cities,
        )

    def submit_tour(self, student_id: str, instance_id: str, tour: list[int]) -> SubmitResult:
        payload = {
            "student_id": student_id,
            "instance_id": instance_id,
            "tour": tour,
        }
        data = self._post_json("/submit", payload)

        in_top_5 = data.get("in_top_5")
        if in_top_5 is None:
            in_top_5 = data.get("in_top5", False)

        return SubmitResult(
            status=data.get("status", "unknown"),
            distance=float(data["distance"]),
            improved=bool(data.get("improved", False)),
            in_top_5=bool(in_top_5),
            rank=data.get("rank"),
        )

    def _get_json(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(url, timeout=self.timeout_s)
        self._raise_for_status(response)
        return response.json()

    def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.post(url, json=payload, timeout=self.timeout_s)
        self._raise_for_status(response)
        return response.json()

    @staticmethod
    def _parse_city(raw_city: list[float] | tuple[float, float]) -> tuple[float, float]:
        if len(raw_city) != 2:
            raise ValueError(f"Invalid city format: {raw_city}")
        lon, lat = raw_city
        return float(lon), float(lat)

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        if response.ok:
            return

        detail = None
        try:
            body = response.json()
            detail = body.get("detail") if isinstance(body, dict) else None
        except ValueError:
            detail = None

        message = detail or response.text or f"HTTP {response.status_code}"
        raise RuntimeError(message)


def to_dict_submit_result(result: SubmitResult) -> dict[str, Any]:
    return asdict(result)
