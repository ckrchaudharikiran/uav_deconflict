from src.core.models import Drone, Mission, Waypoint
from src.core.trajectory import TrajectoryCalculator
from src.core.deconfliction import ConflictDetector
from src.viz.visualizer import Visualizer

def create_demo_scenario():
    # Scenario: Two drones crossing paths in 3D space
    
    # Drone 1: Primary Drone
    # Path: (0,0,0) -> (100, 100, 100)
    mission1 = Mission(waypoints=[
        Waypoint(0, 0, 0),
        Waypoint(80, 100, 100)
    ], start_time=0.0)
    TrajectoryCalculator.assign_times_to_mission(mission1, speed=10.0)
    drone1 = Drone(drone_id="Primary", mission=mission1)

    # Drone 2: Intruder
    # Path: (0, 100, 50) -> (100, 0, 50)
    # They should cross near (50, 50, 50) if z matches, but here z is 50 for drone 2.
    # Drone 1 passes (50, 50, 50) at mid-flight.
    # Drone 2 passes (50, 50, 50) at mid-flight.
    # Conflict expected!
    mission2 = Mission(waypoints=[
        Waypoint(2, 100, 50),
        Waypoint(100, 0, 40)
    ], start_time=0.0)
    TrajectoryCalculator.assign_times_to_mission(mission2, speed=10.0)
    drone2 = Drone(drone_id="Intruder", mission=mission2)

    return drone1, [drone2]

def main():
    print("Initializing UAV Strategic Deconfliction System...")
    
    primary_drone, other_drones = create_demo_scenario()
    
    print(f"Primary Drone Mission Duration: {primary_drone.mission.waypoints[-1].time:.2f}s")
    print(f"Intruder Drone Mission Duration: {other_drones[0].mission.waypoints[-1].time:.2f}s")

    # Detect Conflicts
    detector = ConflictDetector(safety_radius=15.0, time_step=0.5)
    conflicts = detector.check_conflicts(primary_drone, other_drones)

    if conflicts:
        print(f"\n[WARNING] {len(conflicts)} Conflicts Detected!")
        for c in conflicts:
            print(f" - Time: {c['time']:.2f}s, Location: ({c['location'][0]:.1f}, {c['location'][1]:.1f}, {c['location'][2]:.1f}), With: {c['conflicting_drone_id']}, Dist: {c['distance']:.2f}")
    else:
        print("\n[INFO] No conflicts detected. Mission is safe.")

    # Visualize
    print("\nLaunching Visualization...")
    viz = Visualizer([primary_drone] + other_drones, conflicts)
    viz.animate(duration=20.0)

if __name__ == "__main__":
    main()
