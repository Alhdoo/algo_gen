from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0


def haversine_km(city_a: tuple[float, float], city_b: tuple[float, float]) -> float:
    """Compute great-circle distance (km) between two cities given as (lon, lat)."""
    lon_a, lat_a = city_a
    lon_b, lat_b = city_b

    lon_a_rad, lat_a_rad = radians(lon_a), radians(lat_a)
    lon_b_rad, lat_b_rad = radians(lon_b), radians(lat_b)

    dlat = lat_b_rad - lat_a_rad
    dlon = lon_b_rad - lon_a_rad

    a = sin(dlat / 2) ** 2 + cos(lat_a_rad) * cos(lat_b_rad) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def euclidean_km(city_a: tuple[float, float], city_b: tuple[float, float]) -> float:
    """Compute Euclidean distance using Pythagoras on (lon, lat) coordinates."""
    lon_a, lat_a = city_a
    lon_b, lat_b = city_b
    dx = lon_b - lon_a
    dy = lat_b - lat_a
    return sqrt(dx * dx + dy * dy)


def should_use_euclidean(instance_id: str | None) -> bool:
    """Use Euclidean distance for synthetic hard datasets."""
    if not instance_id:
        return False
    return instance_id.startswith("hard")


def tour_distance_km(
    cities: list[tuple[float, float]],
    tour: list[int],
    instance_id: str | None = None,
) -> float:
    """Compute total tour distance, including return to starting city.

    For instance ids starting with "hard", Euclidean distance is used.
    Otherwise, Haversine distance is used.
    """
    if not tour:
        return 0.0

    edge_distance = euclidean_km if should_use_euclidean(instance_id) else haversine_km

    total = 0.0
    n = len(tour)
    for i in range(n):
        a = cities[tour[i]]
        b = cities[tour[(i + 1) % n]]
        total += edge_distance(a, b)
    return total
