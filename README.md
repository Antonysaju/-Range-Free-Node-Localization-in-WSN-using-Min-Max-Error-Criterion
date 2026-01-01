# Range-Free-Node-Localization-in-WSN-using-Min-Max-Error-Criterion
A Python-based simulation that estimates unknown sensor node positions in Wireless Sensor Networks without GPS. Uses a range-free Min–Max Error Criterion with anchor connectivity, error analysis, and real-time mobility visualization for WSN and IoT scenarios.

## How It Works

The localization process is based on a range-free Min–Max Error Criterion:

- Anchor nodes with known positions are deployed in a 2D area.
- Unknown nodes identify anchor nodes within a predefined communication range.
- A bounding box is formed using the minimum and maximum coordinates of reachable anchors.
- The estimated position of an unknown node is computed as the center of the bounding box.
- Localization error is calculated as the Euclidean distance between true and estimated positions.
- The system visualizes localization accuracy, performance trends, and real-time node mobility.

## Output & Results

The project generates a single comprehensive visualization consisting of three components:

- A Localization Map showing anchor nodes, true unknown node positions, and estimated positions using the Min–Max Error Criterion.
- A Performance Analysis Plot illustrating the relationship between communication range and average localization error.
- A Node Mobility Visualization demonstrating real-time tracking of a moving unknown node and its estimated position under noisy conditions.

These visualizations help evaluate the accuracy, behavior, and robustness of the localization approach.
![Output SS](https://github.com/user-attachments/assets/8a6015a1-dc7a-40bc-89fe-3fd1a0ebfc9f)

https://github.com/user-attachments/assets/1734d6e9-c6b3-4c28-9eee-eb7c38f373c7

## How to Run the Project
Ensure that Python is installed and the required libraries are available.
To run the project locally:
  - pip install numpy matplotlib
  - python range_free_localization.py
Ensure that Python is installed and the required libraries are available.


## Technologies Used
- Python
- NumPy
- Matplotlib
- Wireless Sensor Network (WSN) Simulation
- Data Visualization

## Future Scope
- Integrate Machine Learning techniques to reduce localization error using historical data.
- Extend the localization model to 3D environments.
- Deploy the approach in real-time IoT and smart city applications.
- Optimize anchor selection and communication range dynamically for improved accuracy.
