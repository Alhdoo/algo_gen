from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from tsp.api import TSPClient, to_dict_submit_result
from tsp.distance import tour_distance_km
from tsp.solvers import SOLVERS
from tsp.validation import validate_tour

DEFAULT_BASE_URL = "https://tsp-sra0.onrender.com"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="TSP tooling: fetch instances, compute baseline tours, and submit results.",
    )

    parser.add_argument(
        "--base-url",
        default=os.getenv("TSP_BASE_URL", DEFAULT_BASE_URL),
        help="TSP server base URL (env: TSP_BASE_URL)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available instances")

    get_cmd = subparsers.add_parser("get", help="Fetch an instance")
    get_cmd.add_argument("instance_id", help="Instance id, e.g. regions")

    solve_cmd = subparsers.add_parser("solve", help="Compute a tour for an instance")
    solve_cmd.add_argument("instance_id", help="Instance id, e.g. regions")
    solve_cmd.add_argument(
        "--solver",
        default="identity",
        choices=sorted(SOLVERS.keys()),
        help="Solver strategy",
    )

    submit_cmd = subparsers.add_parser("submit", help="Compute and submit a tour")
    submit_cmd.add_argument("instance_id", help="Instance id, e.g. regions")
    submit_cmd.add_argument(
        "--solver",
        default="identity",
        choices=sorted(SOLVERS.keys()),
        help="Solver strategy",
    )
    submit_cmd.add_argument(
        "--student-id",
        default=os.getenv("TSP_STUDENT_ID"),
        help="Student identifier (env: TSP_STUDENT_ID)",
    )

    return parser


def cmd_list(client: TSPClient) -> int:
    instances = client.list_instances()
    payload: dict[str, Any] = {
        instance_id: {
            "name": meta.name,
            "n_cities": meta.n_cities,
        }
        for instance_id, meta in instances.items()
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


def cmd_get(client: TSPClient, instance_id: str) -> int:
    instance = client.get_instance(instance_id)
    payload = {
        "instance_id": instance.instance_id,
        "name": instance.name,
        "cities": [[lon, lat] for lon, lat in instance.cities],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


def solve_instance(client: TSPClient, instance_id: str, solver_name: str) -> tuple[list[int], float]:
    instance = client.get_instance(instance_id)
    solver = SOLVERS[solver_name]
    tour = solver(instance)

    valid, reason = validate_tour(tour, len(instance.cities))
    if not valid:
        raise RuntimeError(f"Invalid tour from solver '{solver_name}': {reason}")

    distance = tour_distance_km(instance.cities, tour, instance.instance_id)
    return tour, distance


def cmd_solve(client: TSPClient, instance_id: str, solver_name: str) -> int:
    tour, distance = solve_instance(client, instance_id, solver_name)
    payload = {
        "instance_id": instance_id,
        "solver": solver_name,
        "distance_km": distance,
        "tour": tour,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


def cmd_submit(client: TSPClient, instance_id: str, solver_name: str, student_id: str | None) -> int:
    if not student_id:
        raise RuntimeError("Missing student id. Use --student-id or TSP_STUDENT_ID.")

    tour, local_distance = solve_instance(client, instance_id, solver_name)
    result = client.submit_tour(student_id=student_id, instance_id=instance_id, tour=tour)

    payload = {
        "student_id": student_id,
        "instance_id": instance_id,
        "solver": solver_name,
        "local_distance_km": local_distance,
        "server": to_dict_submit_result(result),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    client = TSPClient(base_url=args.base_url)

    if args.command == "list":
        return cmd_list(client)
    if args.command == "get":
        return cmd_get(client, args.instance_id)
    if args.command == "solve":
        return cmd_solve(client, args.instance_id, args.solver)
    if args.command == "submit":
        return cmd_submit(client, args.instance_id, args.solver, args.student_id)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
