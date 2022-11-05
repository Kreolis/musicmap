from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from utils.misc import get_dir_root
import networkx as nx

path = get_dir_root()
# read in data
dir_data = path["MSD_tags"]
files = sorted(glob(dir_data + "/*.npy"))
test = np.load(files[0], allow_pickle=True).item()

dir_graph_results = path["graph"]
G = nx.read_adjlist(dir_graph_results + "/cos_sim_songs_graph")
top_tags = np.load(dir_graph_results + "/top_tags.npy")

# create relations for graph
pos = nx.spring_layout(G, seed=1969)  # Seed for reproducible layout

# create color list
clist = [test["tags"].index(tag) for tag in top_tags]
cmap = plt.get_cmap("gist_ncar")
clist = [cmap(ind/len(test["tags"])) for ind in clist]

#Plotting 
options = {"node_color": clist, "node_size": 50, "linewidths": 0, "width": 0.1}
fig, ax = plt.subplots(1)
nx.draw(G, pos, ax=ax, **options)
fig.savefig(dir_graph_results + "/cos_sim_songs_graph")

print()

# OLD
# # define cyclic ordering of tags for color gradient
# G_tags = nx.from_numpy_matrix(cosine_sim_matrix_tags)
# pos = nx.shell_layout(G_tags, [songs[0]["tags"]])
# gradient_order = np.zeros(num_features)
# for i,key in enumerate(pos):
#     gradient_order[i] = np.linalg.norm(pos["guitar"]-pos[key])
# gradient_order = np.argsort(gradient_order)