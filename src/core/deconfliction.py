from typing import List, Dict, Any
import numpy as np
from .models import Drone, Mission
from .trajectory import TrajectoryCalculator

class ConflictDetector:
    def __init__(self, safety_radius: float = 10.0, time_step: float = 0.5):
        self.safety_radius = safety_radius
        self.time_step = time_step

    def check_conflicts(self, primary_drone: Drone, other_drones: List[Drone]) -> List[Dict[str, Any]]:
        """
        Checks for conflicts between the primary drone and other drones.
        Returns a list of conflict details.
        """
        conflicts = []
        
        # Determine the time range to check
        # We check from the start of the primary mission to the end of the primary mission
        start_time = primary_drone.mission.waypoints[0].time
        end_time = primary_drone.mission.waypoints[-1].time
        
        current_time = start_time
        while current_time <= end_time:
            primary_pos = TrajectoryCalculator.calculate_position_at_time(primary_drone.mission, current_time)
            
            if primary_pos is None:
                current_time += self.time_step
                continue

            for other_drone in other_drones:
                other_pos = TrajectoryCalculator.calculate_position_at_time(other_drone.mission, current_time)
                
                if other_pos is not None:
                    dist = self._calculate_distance(primary_pos, other_pos)
                    if dist < self.safety_radius:
                        conflicts.append({
                            "time": current_time,
                            "location": primary_pos,
                            "conflicting_drone_id": other_drone.drone_id,
                            "distance": dist,
                            "type": "Spatial Violation"
                        })
            
            current_time += self.time_step
            
        return conflicts

    def _calculate_distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
