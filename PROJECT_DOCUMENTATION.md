# UAV Strategic Deconfliction System Documentation

## 1. Project Overview

The **UAV Strategic Deconfliction System** is a Python-based simulation framework designed to ensure the safe operation of Unmanned Aerial Vehicles (UAVs) in shared airspace. It provides a 4D (3D space + Time) strategic deconfliction capability, allowing mission planners to validate drone flight paths against the schedules of other drones.

The system's primary goal is to detect and visualize potential conflicts—instances where two drones violate a specified safety radius at the same time—before they occur in reality. This allows for pre-flight adjustment of trajectories to ensure mission safety.

### Key Features
*   **4D Trajectory Modeling**: Accurately models drone positions in x, y, z coordinates over time.
*   **Strategic Conflict Detection**: Identifies spatial violations between drones based on their flight plans.
*   **Interactive Visualization**: Provides a 3D animated view of drone missions and highlights conflict zones.
*   **Extensible Architecture**: Modular design allows for easy integration of new conflict resolution algorithms or more complex drone dynamics.

---

## 2. System Architecture

The project is structured into two main components: the **Core Logic** (`src/core`) and the **Visualization** (`src/viz`).

### 2.1 Core Logic (`src/core`)

This component handles the mathematical and logical operations of the simulation.

*   **`models.py`**: Defines the fundamental data structures used throughout the system.
    *   **`Waypoint`**: Represents a specific point in 4D space (x, y, z, time).
    *   **`Mission`**: A collection of waypoints defining a drone's intended path.
    *   **`Drone`**: An entity representing a UAV, containing its unique ID and assigned mission.

*   **`trajectory.py`**: Responsible for calculating the state of a drone at any given time.
    *   **`TrajectoryCalculator`**: Contains static methods to interpolate drone positions between waypoints. It assumes linear motion between waypoints and handles time assignment based on constant speed.

*   **`deconfliction.py`**: The safety engine of the system.
    *   **`ConflictDetector`**: Iterates through time steps to check for distance violations between a primary drone and other drones in the airspace.

### 2.2 Visualization (`src/viz`)

*   **`visualizer.py`**: Uses `matplotlib` to render the simulation.
    *   **`Visualizer`**: Creates a 3D plot of the airspace, draws the static flight paths, and animates the drones' movement over time. It also visually marks locations where conflicts are detected.

---

## 3. Data Structures & API

### `Waypoint`
```python
@dataclass
class Waypoint:
    x: float
    y: float
    z: float
    time: Optional[float] = None
```
*   **Usage**: Defines a node in the flight path. `time` can be absolute or relative to the mission start.

### `Mission`
```python
@dataclass
class Mission:
    waypoints: List[Waypoint]
    start_time: float = 0.0
    mission_id: str = ""
```
*   **Usage**: Encapsulates the flight plan. `start_time` defines when the drone begins its mission.

### `Drone`
```python
@dataclass
class Drone:
    drone_id: str
    mission: Mission
    priority: int = 1
```
*   **Usage**: The main agent in the simulation.

---

## 4. Key Algorithms

### 4.1 Trajectory Interpolation
The system uses **Linear Interpolation (LERP)** to determine a drone's position between two waypoints.
Given a time $t$ such that $t_{start} \le t \le t_{end}$ for a segment:
1.  Calculate the fraction of the segment completed: $f = \frac{t - t_{start}}{t_{end} - t_{start}}$
2.  Interpolate position: $P(t) = P_{start} + (P_{end} - P_{start}) \times f$

### 4.2 Conflict Detection
The `ConflictDetector` uses a discrete time-stepping approach:
1.  Define a `time_step` (e.g., 0.5s) and a `safety_radius` (e.g., 10m).
2.  Iterate `current_time` from the start to the end of the primary mission.
3.  At each step, calculate the position of the primary drone and all other drones.
4.  Calculate the Euclidean distance $d$ between the primary drone and every other drone.
5.  If $d < \text{safety\_radius}$, record a **Spatial Violation**.

---

## 5. Usage Guide

### 5.1 Prerequisites
*   Python 3.8 or higher
*   `numpy`
*   `matplotlib`

Install dependencies:
```bash
pip install numpy matplotlib
```

### 5.2 Running the Demo
The provided `demo.py` script sets up a scenario with two drones on a collision course.
```bash
python demo.py
```
**Expected Output**:
1.  Console logs indicating mission durations.
2.  A warning listing detected conflicts with timestamps and locations.
3.  A 3D animation window showing the drones moving and a red 'X' appearing at the conflict point.

### 5.3 Creating a Custom Scenario
To create your own simulation, follow this pattern:

```python
from src.core.models import Drone, Mission, Waypoint
from src.core.trajectory import TrajectoryCalculator
from src.core.deconfliction import ConflictDetector
from src.viz.visualizer import Visualizer

# 1. Define Mission
mission = Mission(waypoints=[
    Waypoint(0, 0, 0),
    Waypoint(100, 100, 100)
], start_time=0.0)

# 2. Assign Times (based on speed)
TrajectoryCalculator.assign_times_to_mission(mission, speed=15.0)

# 3. Create Drone
drone = Drone(drone_id="Drone1", mission=mission)

# 4. Detect Conflicts
detector = ConflictDetector(safety_radius=10.0)
conflicts = detector.check_conflicts(drone, [other_drone])

# 5. Visualize
viz = Visualizer([drone, other_drone], conflicts)
viz.animate()
```
