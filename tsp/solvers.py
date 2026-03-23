from __future__ import annotations

from collections.abc import Callable

from .types import InstanceData


def identity_solver(instance: InstanceData) -> list[int]:
    """Return cities in received order: [0, 1, 2, ..., n-1]."""
    return list(range(len(instance.cities)))


SOLVERS: dict[str, Callable[[InstanceData], list[int]]] = {
    "identity": identity_solver,
}
