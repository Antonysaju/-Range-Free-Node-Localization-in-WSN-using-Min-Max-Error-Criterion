# -Range-Free-Node-Localization-in-WSN-using-Min-Max-Error-Criterion
A Python-based simulation that estimates unknown sensor node positions in Wireless Sensor Networks without GPS. Uses a range-free Min–Max Error Criterion with anchor connectivity, error analysis, and real-time mobility visualization for WSN and IoT scenarios.

## How It Works

The localization process is based on a range-free Min–Max Error Criterion:

- Anchor nodes with known positions are deployed in a 2D area.
- Unknown nodes identify anchor nodes within a predefined communication range.
- A bounding box is formed using the minimum and maximum coordinates of reachable anchors.
- The estimated position of an unknown node is computed as the center of the bounding box.
- Localization error is calculated as the Euclidean distance between true and estimated positions.
- The system visualizes localization accuracy, performance trends, and real-time node mobility.
