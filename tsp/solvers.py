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

def hunger_game_random_solver(instance: InstanceData) -> list[int]:
    x: int =500

    solution = random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution)

    for i in range(x):

        s = random_solver(instance)


        score = tour_distance_km(instance.cities, s)

        print(solution_score, score)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution



def best_of_random_solver(instance: InstanceData) -> list[int]:
    out_of: int = 100_000


    solution = hunger_game_random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution)

    print("starting =====")
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


def swap_random_solver(instance: InstanceData) -> list[int]:
    iterations: int = 100_000

    # Start from a decent random solution
    solution = hunger_game_random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution)

    n = len(solution)

    print("======")
    print("start")
    for _ in range(iterations):
        s = solution.copy()

        i, j = random.sample(range(1, n - 1), 2)

        s[i], s[j] = s[j], s[i]

        score = tour_distance_km(instance.cities, s)

        print(solution_score, score)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution


def best_of_random_solver_with_escape(instance: InstanceData) -> list[int]:
    iterations: int = 100_000

    # Initial solution
    current = random_solver(instance)
    current_score = tour_distance_km(instance.cities, current)

    best = current.copy()
    best_score = current_score

    print("starting =====")

    for _ in range(iterations):
        x = random.randint(1, len(current) - 2)

        s = current.copy()

        # Mutation
        if random.random() < 0.5:
            head = s[:x]
            random.shuffle(head)
            s = head + s[x:]
        else:
            tail = s[x:]
            random.shuffle(tail)
            s = s[:x] + tail

        score = tour_distance_km(instance.cities, s)

        print(best_score, current_score, score)

        if score < current_score or (random.random() < 0.001 and current_score - score < 100):
            current = s
            current_score = score

        if score < best_score:
            best = s
            best_score = score

    return best



SOLVERS: dict[str, Callable[[InstanceData], list[int]]] = {
    "identity": identity_solver,
    "random": random_solver,
    "best_random": best_of_random_solver,
    "swap_random": swap_random_solver,
    "best_escape_random": best_of_random_solver_with_escape,

}
