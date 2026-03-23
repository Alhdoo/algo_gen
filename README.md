# TSP Genetic Algorithm - Groundwork

This repository contains a clean foundation for the CPE Lyon TSP assignment.

Current scope:
- API client for `/instances`, `/instances/{id}`, `/submit`
- Haversine distance implementation (km)
- Tour validation (must be a permutation)
- Baseline solver that keeps the exact order received from the server

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI usage

All commands are run from repository root.

List available instances:

```bash
python main.py list
```

Fetch one instance:

```bash
python main.py get regions
```

Compute a baseline tour (same order as received):

```bash
python main.py solve regions --solver identity
```

Submit the baseline tour:

```bash
export TSP_STUDENT_ID="your_student_id"
python main.py submit regions --solver identity
```

If needed, override server URL:

```bash
python main.py --base-url https://tsp-sra0.onrender.com list
```

## Project structure

- `main.py`: CLI entrypoint
- `tsp/api.py`: HTTP client for server endpoints
- `tsp/distance.py`: Haversine and total tour distance
- `tsp/validation.py`: tour integrity checks
- `tsp/solvers.py`: solver registry (currently `identity`)
- `tsp/types.py`: dataclasses for instance and submit payloads

## Next step: genetic algorithm

You can now add your GA in `tsp/solvers.py`, then register it in `SOLVERS`.
The CLI will expose it automatically through `--solver`.
