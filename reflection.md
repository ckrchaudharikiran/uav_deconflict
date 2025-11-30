# Reflection & Justification Document

## Architectural Decisions

### 4D Trajectory Modeling
We chose to model trajectories in 4D (x, y, z, time) to fully satisfy the extra credit requirement and provide a robust solution for real-world scenarios where altitude separation is key.
- **Data Model**: The `Waypoint` class includes an optional `time` attribute. The `TrajectoryCalculator` interpolates between these waypoints.
- **Interpolation**: Linear interpolation was selected for simplicity and efficiency. For more complex flight dynamics, spline interpolation could be added without changing the interface.

### Conflict Detection Strategy
We implemented a discrete time-stepping approach (`ConflictDetector`).
- **Why?**: Analytic solutions for 4D intersection of arbitrary paths can be complex and computationally expensive. Discrete checking is robust, easy to implement, and scales linearly with mission duration.
- **Parameters**: `time_step` (0.5s) and `safety_radius` (10m) are configurable.

### Visualization
We used `matplotlib` for its ubiquity and 3D plotting capabilities. The visualization provides immediate visual feedback on the conflict scenario.

## Scalability Discussion
To scale to tens of thousands of drones, the current O(N*M) approach (checking every drone against every other drone) would be insufficient.

### Proposed Enhancements for Scale
1.  **Spatial Indexing**: Use an R-tree or Octree to index drone trajectories. This allows querying only for trajectories in the vicinity of the primary mission, reducing complexity from O(N) to O(log N).
2.  **Distributed Computing**: Partition the airspace into sectors. Manage each sector with a separate service instance (sharding).
3.  **Real-time Ingestion**: Use a message queue (e.g., Kafka) to handle incoming flight plans and updates asynchronously.
4.  **Database**: Store flight plans in a geospatial database (e.g., PostGIS) to offload some spatial queries.

## AI Integration
AI tools assisted in:
- **Boilerplate Generation**: Rapidly creating data classes

## Testing Strategy
- **Unit Tests**: Verify interpolation logic and distance calculations.
- **Scenario Tests**: The `demo.py` script acts as an integration test, verifying the end-to-end flow from mission definition to conflict detection and visualization.
