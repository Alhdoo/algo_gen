from __future__ import annotations


def validate_tour(tour: list[int], n_cities: int) -> tuple[bool, str | None]:
    """Validate that tour is a permutation of [0..n_cities-1]."""
    if len(tour) != n_cities:
        return False, f"Expected {n_cities} indices, got {len(tour)}"

    if any((not isinstance(i, int)) for i in tour):
        return False, "Tour must contain integers only"

    if any(i < 0 or i >= n_cities for i in tour):
        return False, f"Indices must be in [0, {n_cities - 1}]"

    if len(set(tour)) != n_cities:
        return False, "Each city index must appear exactly once"

    return True, None
