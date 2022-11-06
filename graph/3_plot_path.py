from glob import glob
from os.path import basename
import numpy as np
from utils.misc import get_dir_root
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas

path = get_dir_root()
# read in data
dir_data = path["MSD_tags"]
files = sorted(glob(dir_data + "/*.npy"))
test = np.load(files[0], allow_pickle=True).item()
tag_options = np.asarray(test["tags"])


dir_graph_results = path["graph"]
for key in ["max", "mean"]:

    G = nx.read_adjlist(dir_graph_results + f"/cos_sim_songs_graph_{key}")
    feature_array = np.load(dir_graph_results + f"/feature_array_{key}.npy")
    logits_array = np.load(dir_graph_results + "/logits_array.npy")

    # Define start and end genre 
    start_key = 'Mellow'
    end_key = 'party'
    # find index
    start_ind = np.where(tag_options == start_key)[0][0]
    end_ind = np.where(tag_options == end_key)[0][0]
    # get ind-most probable song
    ind = 10
    start_song = np.argsort(logits_array[:,start_ind])[-ind]
    end_song = np.argsort(logits_array[:,end_ind])[-ind]

    # find path between start adn end song with specified length
    k_hops = 10
    all_path = nx.all_simple_paths(G, source=str(start_song), target=str(end_song), cutoff=k_hops)
    k_hop_paths = []
    for path in all_path:
        if len(path) == k_hops+1:
            k_hop_paths.append(path)
            break

    # pick random path of specified length
    path = random.choice(k_hop_paths)
    path_edges = []
    for n in range(len(path)-1):
        edge = (path[n], path[n+1])
        path_edges.append(edge)
        
    #Plotting
    pos = nx.spring_layout(G, seed=1)  # Seed for reproducible layout
    options = {"edge_color":"w", "node_size": 10, "linewidths": 0, "width": 0.01}
    fig, ax = plt.subplots(1)
    nx.draw(G, pos, ax=ax, **options)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=path_edges,
        width=2,
        alpha=0.5,
        edge_color="tab:red",
    )
    fig.savefig(dir_graph_results + f"/{start_key}_to_{end_key}_spring_layout_{key}", dpi=300, transparent=True)

    # save playlist
    play_list = []
    for node in path:
        filename = basename(files[int(node)])
        play_list.append(filename)
    np.save(dir_graph_results + f"/{start_key}_to_{end_key}_play_list_{key}", play_list)

print()