import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import zoom

# Data setup
time_slots = [f"{h:02}:{m:02}" for h in range(24) for m in [0, 30]]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
streamer = "Streamer Name"

np.random.seed(0)
data = np.random.rand(7, 48)

# Interpolate each row horizontally
zoom_factor = 10
interpolated_rows = [np.expand_dims(zoom(row, zoom_factor, order=3), axis=0) for row in data]
interpolated_data = np.vstack(interpolated_rows)

# --- Custom Colormap ---
colors = [
    (0.0, "#242429"),   # 0% - 10% = gray
    (0.1, "#242429"),   # gray
    (0.3, "#00ff00"),   # green
    (0.7, "#ffff00"),   # yellow
    (1.0, "#ff0000"),   # red
]
custom_cmap = LinearSegmentedColormap.from_list("custom_heatmap", colors)

# --- Plot ---
plt.figure(figsize=(20, 6))
plt.imshow(interpolated_data, aspect="auto", cmap=custom_cmap, interpolation="none")

# Black background, white text
plt.gca().set_facecolor("#121214")
plt.gcf().patch.set_facecolor("#121214")
plt.xticks(color="white")
plt.yticks(color="white")
plt.xlabel("Time of Day", color="white")
plt.ylabel("Day of Week", color="white")
plt.title(f"Streamer Probability Heatmap of {streamer}", color="white")

# X ticks
num_slots = len(time_slots)
x_res = num_slots * zoom_factor
xtick_positions = np.linspace(0, x_res, num_slots)[::4]
xtick_labels = time_slots[::4]
plt.xticks(ticks=xtick_positions, labels=xtick_labels, rotation=45)

# Y ticks
ytick_positions = np.arange(len(days))
plt.yticks(ticks=ytick_positions, labels=days)

# Colorbar
cbar = plt.colorbar()
cbar.set_label("Chance Streamer is Online", color="white")
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

# Save image
plt.tight_layout()
plt.show()
# plt.savefig("streamer_heatmap_custom_colors.png", dpi=300, facecolor="black")
# plt.close()
