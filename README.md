# UAV Strategic Deconfliction System

A 4D (3D space + Time) strategic deconfliction system for UAVs. This system validates drone missions against simulated flight schedules of other drones to ensure safety in shared airspace.

## Features
- **4D Trajectory Modeling**: Supports x, y, z coordinates and time.
- **Conflict Detection**: Checks for spatial and temporal violations using a configurable safety radius.
- **Visualization**: 3D animation of drone flights with conflict highlighting.

## Setup

1.  **Prerequisites**: Python 3.8+
2.  **Install Dependencies**:
    ```bash
    pip install numpy matplotlib
    ```

## Usage

Run the demo script to see a simulated conflict scenario:

```bash
python demo.py
```

## Project Structure
- `src/core`: Core logic for data models, trajectory calculation, and conflict detection.
- `src/viz`: Visualization tools using Matplotlib.
- `demo.py`: Main entry point for the demonstration.

## Design Decisions
- **Time Discretization**: We use discrete time stepping for conflict detection to handle complex trajectories robustly.
- **Interpolation**: Linear interpolation is used between waypoints.
