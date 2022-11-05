from glob import glob
import numpy as np
from utils.misc import get_dir_root
import networkx as nx
import random
import matplotlib.pyplot as plt

path = get_dir_root()
# read in data
dir_data = path["MSD_tags"]
files = sorted(glob(dir_data + "/*.npy"))
test = np.load(files[0], allow_pickle=True).item()

dir_graph_results = path["graph"]
G = nx.read_adjlist(dir_graph_results + "/cos_sim_songs_graph")
feature_array = np.load(dir_graph_results + "/feature_array.npy")

#Find start and end indices 
tag_options = np.asarray(test["tags"])

#Can change these to 'happy'/ 'sad' 
start_key = 'sad'
end_key = 'happy'

start_ind = np.where(tag_options == start_key)[0][0]
end_ind = np.where(tag_options == end_key)[0][0]

ind = 10
start_song = np.argsort(feature_array[:,start_ind])[-ind]
end_song = np.argsort(feature_array[:,end_ind])[-ind]

k_hops = 10
all_path = nx.all_simple_paths(G, source=str(start_song), target=str(end_song), cutoff=k_hops)
k_hop_paths = []
for path in all_path:
    if len(path) == k_hops+1:
        k_hop_paths.append(path)

# pick random path of specified length
path = random.choice(k_hop_paths)
path_edges = []
for n in range(len(path)-1):
    edge = (path[n], path[n+1])
    path_edges.append(edge)
    
#Plotting
pos = nx.spring_layout(G, seed=1969)  # Seed for reproducible layout
options = {"node_size": 50, "linewidths": 0, "width": 0.1}
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
fig.savefig(dir_graph_results + "/sad_to_happy")

print()