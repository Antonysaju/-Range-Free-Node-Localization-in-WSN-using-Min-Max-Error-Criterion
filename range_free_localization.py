"""
Range-Free Localization using Min–Max Error Criterion
Author: Antony Saju David & Adithya A
Year/Sec: Final Year / CSE
Date: October 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------- UTILITY FUNCTIONS --------------------
def generate_nodes(area_width, area_height, num_anchors, num_unknowns):
    anchors = np.random.rand(num_anchors, 2) * [area_width, area_height]
    unknowns = np.random.rand(num_unknowns, 2) * [area_width, area_height]
    return anchors, unknowns

def estimate_position_minmax_inrange(anchors, comm_range, node):
    # Select only anchors within communication range
    distances = np.linalg.norm(anchors - node, axis=1)
    in_range = anchors[distances <= comm_range]
    if len(in_range) == 0:
        return np.array([np.nan, np.nan])
    # Min-max bounding box
    min_x, max_x = np.min(in_range[:,0]), np.max(in_range[:,0])
    min_y, max_y = np.min(in_range[:,1]), np.max(in_range[:,1])
    return np.array([(min_x + max_x)/2, (min_y + max_y)/2])

def estimate_position_minmax(anchors, distances):
    # Used for mobility plot and performance evaluation
    x_min, y_min = np.min(anchors[:, 0] - distances), np.min(anchors[:, 1] - distances)
    x_max, y_max = np.max(anchors[:, 0] + distances), np.max(anchors[:, 1] + distances)
    return np.array([(x_min + x_max)/2, (y_min + y_max)/2])

def simulate_localization(area_width, area_height, num_anchors, num_unknowns, comm_range, noise):
    anchors, unknowns = generate_nodes(area_width, area_height, num_anchors, num_unknowns)
    estimated = []
    errors = []

    for u in unknowns:
        true_distances = np.linalg.norm(anchors - u, axis=1)
        # Consider only anchors within the preset communication range
        in_range = anchors[true_distances <= comm_range]
        if len(in_range) == 0:
            estimated.append([np.nan, np.nan])
            errors.append(np.nan)
            continue
        # Use min-max based on in_range anchors
        x_min, y_min = np.min(in_range[:, 0]), np.min(in_range[:, 1])
        x_max, y_max = np.max(in_range[:, 0]), np.max(in_range[:, 1])
        estimated_pos = np.array([(x_min + x_max)/2, (y_min + y_max)/2])
        estimated.append(estimated_pos)
        errors.append(np.linalg.norm(u - estimated_pos))

    return anchors, unknowns, np.array(estimated), np.array(errors)

def average_error(area_width, area_height, num_anchors, num_unknowns, comm_range, noise, trials):
    errors = []
    for _ in range(trials):
        _, _, _, e = simulate_localization(area_width, area_height, num_anchors, num_unknowns, comm_range, noise)
        if len(e) > 0:
            errors.extend(e)
    return np.mean(errors) if len(errors) > 0 else np.nan

# -------------------- VISUALIZATION --------------------
def plot_results(anchors, unknowns, estimated, errors, avg_error, comm_range, area_width, area_height, noise):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Range-Free Localization using Min–Max Error Criterion", fontsize=14, fontweight="bold")

    # ----- Plot 1: Node Placement + Error Lines (Old Logic) -----
    ax1 = axes[0]
    ax1.scatter(anchors[:,0], anchors[:,1], c='blue', marker='^', s=120, label='Anchors')
    ax1.scatter(unknowns[:,0], unknowns[:,1], c='green', s=60, label='True Unknowns')
    ax1.scatter(estimated[:,0], estimated[:,1], c='red', marker='x', s=80, label='Estimated')

    # Draw lines and show errors
    for i, (u, e, err) in enumerate(zip(unknowns, estimated, errors)):
        ax1.plot([u[0], e[0]], [u[1], e[1]], color='grey', linestyle='--', alpha=0.6)
        if i < 3:  # show error only for first 3 unknowns
            ax1.text((u[0]+e[0])/2 + 0.5, (u[1]+e[1])/2 + 0.5, f"{err:.2f} m",
                    fontsize=8, color='grey')

    ax1.set_title(f"Localization Map\nAvg Error: {avg_error:.2f} m")
    ax1.set_xlabel("X Position (m)")
    ax1.set_ylabel("Y Position (m)")
    ax1.legend()
    ax1.grid(True)
    ax1.set_xlim(0, area_width)
    ax1.set_ylim(0, area_height)

    # ----- Plot 2: Performance Evaluation -----
    ax2 = axes[1]
    comm_ranges = [comm_range/2, comm_range, comm_range*1.5, comm_range*2]
    perf_errors = []
    for r in comm_ranges:
        # Single simulation per range (instead of averaging) for consistent trend
        a, u, est, err = simulate_localization(area_width, area_height, num_anchors, num_unknowns, r, noise)
        perf_errors.append(np.mean(err))
    ax2.plot(comm_ranges, perf_errors, marker='o', color='purple')
    ax2.set_title("Performance vs Communication Range")
    ax2.set_xlabel("Communication Range (m)")
    ax2.set_ylabel("Average Localization Error (m)")
    ax2.grid(True)

    # ----- Plot 3: Mobility Simulation -----
    ax3 = axes[2]
    ax3.set_xlim(0, area_width)
    ax3.set_ylim(0, area_height)
    ax3.set_title("Node Mobility (Live Visualization)")
    ax3.set_xlabel("X Position (m)")
    ax3.set_ylabel("Y Position (m)")

    anchor_plot, = ax3.plot(anchors[:,0], anchors[:,1], 'bs', label='Anchors')
    target_plot, = ax3.plot([], [], 'go', label='Moving Unknown')
    est_plot, = ax3.plot([], [], 'rx', label='Estimated')
    ax3.legend()

    path_x = np.linspace(10, area_width-10, 80)
    path_y = area_height/2 + 15 * np.sin(np.linspace(0, 4*np.pi, 80))

    def update(frame):
        target = np.array([path_x[frame], path_y[frame]])
        true_distances = np.linalg.norm(anchors - target, axis=1)
        noisy_distances = true_distances + np.random.normal(0, noise, len(true_distances))
        est = estimate_position_minmax(anchors, noisy_distances)
        target_plot.set_data([target[0]], [target[1]])
        est_plot.set_data([est[0]], [est[1]])
        return target_plot, est_plot

    ani = FuncAnimation(fig, update, frames=len(path_x), interval=150, blit=True, repeat=True)

    plt.tight_layout()
    plt.show()

# -------------------- MAIN EXECUTION --------------------
if __name__ == "__main__":
    print("\n🔹 Range-Free Localization using Min–Max Error Criterion 🔹")
    print("------------------------------------------------------------")

    # Preset values
    comm_range = 50       # meters
    noise = 1.0           # low noise for accuracy
    trials = 25           # average over 25 simulations

    # User input for flexible parameters
    area_width = float(input("Enter area width (e.g., 100): "))
    area_height = float(input("Enter area height (e.g., 100): "))
    num_anchors = int(input("Enter number of anchor nodes (e.g., 10): "))
    num_unknowns = int(input("Enter number of unknown nodes to locate (e.g., 3): "))

    print("\nRunning performance evaluation...\n")

    # Single iteration for first plot
    anchors, unknowns, estimated, errors = simulate_localization(area_width, area_height,
                                                                 num_anchors, num_unknowns,
                                                                 comm_range, noise)
    avg_error = np.mean(errors)
    print(f"Average localization error: {avg_error:.2f} m")

    print("\nGenerating visualization plots...\n")
    plot_results(anchors, unknowns, estimated, errors, avg_error, comm_range, area_width, area_height, noise)

    print("\n✅ Simulation complete.")