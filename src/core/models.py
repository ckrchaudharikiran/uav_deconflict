from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class Waypoint:
    x: float
    y: float
    z: float
    time: Optional[float] = None  # Time in seconds from mission start

@dataclass
class Mission:
    waypoints: List[Waypoint]
    start_time: float = 0.0  # Absolute start time or relative to simulation start
    mission_id: str = ""

@dataclass
class Drone:
    drone_id: str
    mission: Mission
    priority: int = 1 # Lower number means higher priority (optional for future use)
