from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from utils.misc import get_dir_root
import networkx as nx
from os.path import basename

path = get_dir_root()
# read in data
dir_data = path["MSD_tags"]
files = sorted(glob(dir_data + "/*.npy"))
test = np.load(files[0], allow_pickle=True).item()

dir_graph_results = path["graph"]

for key in ["max", "mean"]:
    G = nx.read_adjlist(dir_graph_results + f"/cos_sim_songs_graph_{key}")
    top_tags = np.load(dir_graph_results + "/top_tags.npy")

    # create relations for graph
    pos = nx.spring_layout(G, seed=1969)  # Seed for reproducible layout

    # create color list
    clist = [test["tags"].index(tag) for tag in top_tags]
    cmap = plt.get_cmap("gist_ncar")
    clist = [cmap(ind/len(test["tags"])) for ind in clist]

    #Plotting 
    options = {"node_color": clist, "node_size": 10, "linewidths": 0, "width": 0.1}
    fig, ax = plt.subplots(1)
    nx.draw(G, pos, ax=ax, **options)
    fig.savefig(dir_graph_results + f"/cos_sim_songs_graph_{key}", dpi=300)

    # create dictionary with position
    pos_dict = {}
    for f, file in enumerate(files):
        filename = basename(file)
        pos_dict[filename] = pos[str(f)]
    np.save(dir_graph_results + f"/pos_dict_{key}", pos_dict)

print()