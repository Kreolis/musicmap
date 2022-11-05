from os.path import dirname
import numpy as np
import matplotlib.pyplot as plt

# read in data
file_path = "/home/oberlav1/scratch/graphics/oberlav1/junction22/global_outputs.npy"
cosine_sim_matrix = np.load(dirname(file_path) + "/cosine_sim_matrix.npy")

fig, ax = plt.subplots(1, figsize=(4,4))
ax.set_title("Cosine similarity matrix adjacency ",fontsize=12)
ax.imshow(cosine_sim_matrix)
fig.savefig(dirname(file_path) + "/cosine_sim_matrix.png")


print()
