from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from .types import InstanceData
from .distance import tour_distance_km
import random


def _plot_scores(
    instance_id: str,
    best_scores: list[float],
    current_scores: list[float],
    candidate_scores: list[float],
) -> None:
    """Save score curves for offline inspection after a solver run."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed; skipping score plot")
        return

    output_dir = Path("plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{instance_id}_section_scores.png"

    x = list(range(len(best_scores)))
    plt.figure(figsize=(12, 6))
    plt.plot(x, best_scores, label="best_score", linewidth=2)
    plt.plot(x, current_scores, label="current_score", linewidth=1)
    plt.plot(x, candidate_scores, label="score", linewidth=1, alpha=0.7)
    plt.xlabel("iteration")
    plt.ylabel("distance")
    plt.title(f"Score evolution - {instance_id} (section solver)")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"score plot saved: {output_path}")

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
    solution_score = tour_distance_km(instance.cities, solution, instance.instance_id)

    for i in range(x):

        s = random_solver(instance)


        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(solution_score, score)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution

def best_of_random_solver(instance: InstanceData) -> list[int]:
    out_of: int = 100_000


    solution = hunger_game_random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution, instance.instance_id)

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

        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(solution_score, score, x)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution

def swap_random_solver(instance: InstanceData) -> list[int]:
    iterations: int = 100_000

    # Start from a decent random solution
    solution = hunger_game_random_solver(instance)
    solution_score = tour_distance_km(instance.cities, solution, instance.instance_id)

    n = len(solution)

    print("======")
    print("start")
    for _ in range(iterations):
        s = solution.copy()

        i, j = random.sample(range(1, n - 1), 2)

        s[i], s[j] = s[j], s[i]

        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(solution_score, score)
        if score < solution_score:
            solution = s
            solution_score = score

    return solution

def best_of_random_solver_with_escape(instance: InstanceData) -> list[int]:
    iterations: int = 100_000

    # Initial solution
    current = random_solver(instance)
    current_score = tour_distance_km(instance.cities, current, instance.instance_id)

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

        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(best_score, current_score, score)

        if score < current_score or (random.random() < 0.001 and current_score - score < 100):
            current = s
            current_score = score

        if score < best_score:
            best = s
            best_score = score

    return best

def best_of_random_solver_section(instance: InstanceData) -> list[int]:
    iterations: int = 1000000

    # Initial solution
    current = random_solver(instance)
    current_score = tour_distance_km(instance.cities, current, instance.instance_id)

    best = current.copy()
    best_score = current_score

    best_scores: list[float] = [best_score]
    current_scores: list[float] = [current_score]
    candidate_scores: list[float] = [current_score]

    print("starting =====")

    n = len(current)

    for _ in range(iterations):
        s = current.copy()

        i, j = sorted(random.sample(range(1, n - 1), 2))
        section = s[i:j]

        random.shuffle(section)
        s[i:j] = section

        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(best_score, current_score, score)

        best_scores.append(best_score)
        current_scores.append(current_score)
        candidate_scores.append(score)

        if score < current_score or (random.random() < 0.001 and score - current_score < 100):
            current = s
            current_score = score

        if score < best_score:
            best = s
            best_score = score

    _plot_scores(instance.instance_id, best_scores, current_scores, candidate_scores)

    return best


SOLVERS: dict[str, Callable[[InstanceData], list[int]]] = {
    "identity": identity_solver,
    "random": random_solver,
    "best_random": best_of_random_solver,
    "swap_random": swap_random_solver,
    "best_escape_random": best_of_random_solver_with_escape,
    "section": best_of_random_solver_section,

}
