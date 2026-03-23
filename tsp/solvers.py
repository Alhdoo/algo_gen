from __future__ import annotations

from collections.abc import Callable

from .types import InstanceData
from .distance import tour_distance_km
import random

def identity_solver(instance: InstanceData) -> list[int]:
    """Return cities in received order: [0, 1, 2, ..., n-1]."""
    return list(range(len(instance.cities)))


def random_solver(instance: InstanceData) -> list[int]:
    """Return a random tour."""
    import random

    tour = list(range(len(instance.cities)))
    random.shuffle(tour)
    return tour


def best_of_random_solver(instance: InstanceData) -> list[int]:
    out_of: int = 100_000

    solution = random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution)

    for _ in range(out_of):
        x = random.randint(1, len(solution) - 2) 

        s = solution.copy()

        if random.random() < 0.5:
            head = s[:x]
            random.shuffle(head)
            s = head + s[x:]
        else:
            tail = s[x:]
            random.shuffle(tail)
            s = s[:x] + tail

        score = tour_distance_km(instance.cities, s)

        print(solution_score, score, x)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution



SOLVERS: dict[str, Callable[[InstanceData], list[int]]] = {
    "identity": identity_solver,
    "random": random_solver,
    "best_random": best_of_random_solver
}
