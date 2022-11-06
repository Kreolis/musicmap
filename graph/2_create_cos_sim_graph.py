from glob import glob
import numpy as np
from scipy import spatial
from utils.misc import get_dir_root
import networkx as nx

path = get_dir_root()
# read in data
dir_data = path["graph"]
for key in ["max", "mean"]:
    cos_sim_songs = np.load(dir_data + f"/cos_sim_songs_{key}.npy")

    # create upper triangle graph
    n = cos_sim_songs.shape[0]
    triu_ind = np.triu_indices(n)
    cosine_sim_mask = cos_sim_songs.copy()
    cosine_sim_mask[triu_ind] = np.nan

    # threshold to sparsify matrix
    percentage = 0.97
    n_egde_keep = int(len(cos_sim_songs) *(1-percentage))

    # only % most similar songs 
    G = nx.Graph()
    G.clear()
    n = len(cos_sim_songs)
    for i in range(n):
        threshold = np.sort(cos_sim_songs[i,:])[-n_egde_keep]
        for j in range(n):
            not_self_loop = i != j
            above_threshold = cos_sim_songs[i,j] > threshold
            double_connection = np.isnan(cosine_sim_mask[i,j])
            if (not_self_loop and above_threshold): #  and not double_connection
                G.add_edge(i,j,weight=cos_sim_songs[i,j])

    nx.write_adjlist(G, dir_data + f"/cos_sim_songs_graph_{key}")

print()