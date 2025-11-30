import numpy as np
from typing import Tuple, Optional
from .models import Mission, Waypoint

class TrajectoryCalculator:
    @staticmethod
    def calculate_position_at_time(mission: Mission, t: float) -> Optional[Tuple[float, float, float]]:
        """
        Calculates the (x, y, z) position of the drone at absolute time t.
        Returns None if t is outside the mission duration.
        """
        waypoints = mission.waypoints
        if not waypoints:
            return None

        # Adjust time to be relative to mission start if needed, 
        # but here we assume waypoint.time is absolute or relative to the same reference as t.
        # Let's assume waypoint.time is relative to mission.start_time for the input,
        # but for calculation we need a common time frame.
        # SIMPLIFICATION: We will assume waypoint.time is the absolute time for that waypoint.
        
        # Check if t is before start or after end
        if t < waypoints[0].time or t > waypoints[-1].time:
            return None

        # Find the segment [wp_prev, wp_next] that contains t
        for i in range(len(waypoints) - 1):
            wp_start = waypoints[i]
            wp_end = waypoints[i+1]

            if wp_start.time <= t <= wp_end.time:
                # Interpolate
                dt_segment = wp_end.time - wp_start.time
                if dt_segment <= 0:
                    return (wp_start.x, wp_start.y, wp_start.z) # Instant jump or zero time segment

                fraction = (t - wp_start.time) / dt_segment
                
                x = wp_start.x + (wp_end.x - wp_start.x) * fraction
                y = wp_start.y + (wp_end.y - wp_start.y) * fraction
                z = wp_start.z + (wp_end.z - wp_start.z) * fraction
                
                return (x, y, z)

        return None

    @staticmethod
    def assign_times_to_mission(mission: Mission, speed: float):
        """
        Helper to assign timestamps to waypoints based on constant speed,
        starting from mission.start_time.
        """
        if not mission.waypoints:
            return

        current_time = mission.start_time
        mission.waypoints[0].time = current_time

        for i in range(len(mission.waypoints) - 1):
            p1 = mission.waypoints[i]
            p2 = mission.waypoints[i+1]
            
            dist = np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2)
            time_leg = dist / speed
            
            current_time += time_leg
            p2.time = current_time
