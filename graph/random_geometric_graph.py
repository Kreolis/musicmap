from os.path import dirname
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# convert cosine similarity matrix to graph
file_path = "/home/oberlav1/scratch/graphics/oberlav1/junction22/global_outputs.npy"
cosine_sim_matrix = np.load(dirname(file_path) + "/cosine_sim_matrix.npy")

# create upper triangle graph
n = cosine_sim_matrix.shape[0]
triu_ind = np.triu_indices(n)
cosine_sim_mask = cosine_sim_matrix.copy()
cosine_sim_mask[triu_ind] = np.nan

# threshold to sparsify matrix
factor = 0.9
threshold = (cosine_sim_matrix.max() - cosine_sim_matrix.min()) * factor
inds = np.where(cosine_sim_matrix > threshold)
i, j = np.unravel_index(inds, cosine_sim_matrix.shape)

 # only 8 "strongest" neighbors
G = nx.Graph()
G.clear()
n = len(cosine_sim_matrix)
for i in range(n):
    for j in range(n):
        if ((i != j) and (cosine_sim_matrix[i,j] > threshold) and not (np.isnan(cosine_sim_mask[i,j]))):
            G.add_edge(i,j,weight=cosine_sim_matrix[i,j])

options = {"node_color": "black", "node_size": 50, "linewidths": 0, "width": 0.1}

pos = nx.spring_layout(G, seed=1969)  # Seed for reproducible layout
nx.draw(G, pos, **options)
plt.show()

plt.savefig(dirname(file_path) + "/cosine_network")

print()