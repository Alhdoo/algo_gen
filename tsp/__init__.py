"""TSP toolkit: API client, distance utilities, validators, and solver scaffolding."""

from .api import TSPClient
from .distance import haversine_km, tour_distance_km
from .solvers import identity_solver
from .types import InstanceData
from .validation import validate_tour

__all__ = [
    "TSPClient",
    "InstanceData",
    "haversine_km",
    "tour_distance_km",
    "validate_tour",
    "identity_solver",
]
