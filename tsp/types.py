from __future__ import annotations

from dataclasses import dataclass


City = tuple[float, float]  # (longitude, latitude)


@dataclass(frozen=True)
class InstanceMetadata:
    name: str
    n_cities: int


@dataclass(frozen=True)
class InstanceData:
    instance_id: str
    name: str
    cities: list[City]


@dataclass(frozen=True)
class SubmitResult:
    status: str
    distance: float
    improved: bool
    in_top_5: bool
    rank: int | None
