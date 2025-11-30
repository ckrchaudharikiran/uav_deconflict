import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Dict, Any
import numpy as np
from ..core.models import Drone
from ..core.trajectory import TrajectoryCalculator

class Visualizer:
    def __init__(self, drones: List[Drone], conflicts: List[Dict[str, Any]] = None):
        self.drones = drones
        self.conflicts = conflicts if conflicts else []
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.lines = {}
        self.points = {}
        self.conflict_points = []

    def setup_plot(self):
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('UAV Strategic Deconfliction Simulation (4D)')
        
        # Determine bounds
        all_x, all_y, all_z = [], [], []
        for drone in self.drones:
            for wp in drone.mission.waypoints:
                all_x.append(wp.x)
                all_y.append(wp.y)
                all_z.append(wp.z)
        
        margin = 10
        self.ax.set_xlim(min(all_x)-margin, max(all_x)+margin)
        self.ax.set_ylim(min(all_y)-margin, max(all_y)+margin)
        self.ax.set_zlim(min(all_z)-margin, max(all_z)+margin)

        # Draw static paths
        colors = ['b', 'g', 'c', 'm', 'y', 'k']
        for i, drone in enumerate(self.drones):
            color = colors[i % len(colors)]
            xs = [wp.x for wp in drone.mission.waypoints]
            ys = [wp.y for wp in drone.mission.waypoints]
            zs = [wp.z for wp in drone.mission.waypoints]
            self.ax.plot(xs, ys, zs, color=color, linestyle='--', alpha=0.5, label=f'Drone {drone.drone_id}')
            
            # Initialize moving points
            point, = self.ax.plot([], [], [], 'o', color=color, markersize=8)
            self.points[drone.drone_id] = point

        self.ax.legend()

    def update(self, frame, start_time, time_step):
        current_time = start_time + frame * time_step
        self.ax.set_title(f'Time: {current_time:.2f}s')

        # Update drone positions
        for drone in self.drones:
            pos = TrajectoryCalculator.calculate_position_at_time(drone.mission, current_time)
            if pos:
                self.points[drone.drone_id].set_data([pos[0]], [pos[1]])
                self.points[drone.drone_id].set_3d_properties([pos[2]])
            else:
                # Hide if not flying
                self.points[drone.drone_id].set_data([], [])
                self.points[drone.drone_id].set_3d_properties([])

        # Highlight conflicts
        # Remove old conflict markers
        for cp in self.conflict_points:
            cp.remove()
        self.conflict_points.clear()

        for conflict in self.conflicts:
            # Show conflict if it's happening "now" (within a small window)
            if abs(conflict['time'] - current_time) < time_step:
                loc = conflict['location']
                cp = self.ax.scatter([loc[0]], [loc[1]], [loc[2]], color='r', s=100, marker='x', label='Conflict')
                self.conflict_points.append(cp)

    def animate(self, duration=20, time_step=0.1):
        self.setup_plot()
        
        # Determine start time
        start_time = min(d.mission.waypoints[0].time for d in self.drones if d.mission.waypoints)
        
        frames = int(duration / time_step)
        
        ani = animation.FuncAnimation(
            self.fig, 
            self.update, 
            frames=frames, 
            fargs=(start_time, time_step), 
            interval=50, 
            blit=False
        )
        
        plt.show()
