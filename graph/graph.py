import os, random
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
import networkx as nx
from .utils.misc import get_dir_root
from os.path import basename
from typing import List

def compute_cosine_sim(file_folder:str):

    path = get_dir_root(file_folder)
    # read in data
    dir_data = path["MSD_tags"]
    dir_out = path["graph"]
    pp = os.path.join(dir_data, "*.npy")
    files = sorted(glob(pp))
    num_songs = len(files)

    test = np.load(files[0], allow_pickle=True).item()
    num_features = test["features"]["max_pool"].shape[-1]
    num_logits = len(test["tags"])

    feature_array = np.zeros((num_songs, num_features))
    logits_array = np.zeros((num_songs, num_logits))
    top_tags = [None]*num_songs
    for i, file in enumerate(files):
        temp = np.load(file, allow_pickle=True).item()
        feature_array[i, :] = np.max(temp["features"]["max_pool"], axis=0)
        logits_array[i,:] = np.mean(temp["taggram"], axis=0)
        max_logit = np.argmax(logits_array[i,:])
        top_tags[i] = temp["tags"][max_logit]

        
    np.save(os.path.join(dir_out, "feature_array_max"), feature_array)
    np.save(os.path.join(dir_out, "logits_array"), logits_array)
    np.save(os.path.join(dir_out, "top_tags"), top_tags)

    # cosine similarity betweeen songs
    cos_sim_songs = np.zeros((num_songs, num_songs)) 
    for i in range(num_songs):
        for j in range(num_songs):
            cos_sim_songs[i,j] = 1 - spatial.distance.cosine(feature_array[i,:], feature_array[j,:])

    np.save(os.path.join(dir_out, f"cos_sim_songs"), cos_sim_songs)

    # cosine similarity betweeen tags
    cos_sim_tags = np.zeros((num_features, num_features)) 
    for i in range(num_features):
        for j in range(num_features):
            cos_sim_tags[i,j] = 1 - spatial.distance.cosine(feature_array[:,i], feature_array[:,j])

    np.save(os.path.join(dir_out, f"cos_sim_tags"), cos_sim_tags)

    # PLOTTING
    """
    fig, ax = plt.subplots(1)
    ax.set_title("Cosine similarity between songs ",fontsize=12)
    ax.imshow(cos_sim_songs)
    fig.savefig(os.path.join(dir_out, f"cos_sim_songs.png"))

    fig, ax = plt.subplots(1)
    ax.set_title("Cosine similarity between tags ",fontsize=12)
    ax.imshow(cos_sim_tags)
    fig.savefig(os.path.join(dir_out, f"cos_sim_tags.png"))
    """
    print()


def create_cos_graph(file_folder:str):
    path = get_dir_root(file_folder)
    # read in data
    dir_data = path["graph"]
    cos_sim_songs = np.load(os.path.join(dir_data, f"cos_sim_songs.npy"))

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

    nx.write_adjlist(G, os.path.join(dir_data, f"cos_sim_songs_graph"))

    print()

def calc_path(file_folder:str, k_hops: int = 10, start_tag: str = 'Mellow', end_tag:str = 'party'):
    path = get_dir_root(file_folder)
    # read in data
    dir_data = path["MSD_tags"]
    files = sorted(glob(os.path.join(dir_data, "*.npy")))
    test = np.load(files[0], allow_pickle=True).item()
    tag_options = np.asarray(test["tags"])


    dir_graph_results = path["graph"]

    G = nx.read_adjlist(os.path.join(dir_graph_results, f"cos_sim_songs_graph"))
    #feature_array = np.load(os.path.join(dir_graph_results, f"feature_array.npy"))
    logits_array = np.load(os.path.join(dir_graph_results, "logits_array.npy"))

    # Define start and end genre 
    start_tag = 'Mellow'
    end_tag = 'party'
    # find index
    start_ind = np.where(tag_options == start_tag)[0][0]
    end_ind = np.where(tag_options == end_tag)[0][0]
    # get ind-most probable song
    ind = 10
    start_song = np.argsort(logits_array[:,start_ind])[-ind]
    end_song = np.argsort(logits_array[:,end_ind])[-ind]

    # find path between start adn end song with specified length
    all_path = nx.all_simple_paths(G, source=str(start_song), target=str(end_song), cutoff=k_hops)
    k_hop_paths = []
    for path in all_path:
        if len(path) == k_hops+1:
            k_hop_paths.append(path)
            if len(k_hop_paths) > 50:
                break

    # pick random path of specified length
    path = random.choice(k_hop_paths)
    path_edges = []
    for n in range(len(path)-1):
        edge = (path[n], path[n+1])
        path_edges.append(edge)
    
    return G, path, path_edges, files

def plot_graph(G, path_edges, filename: str = None, save_figure: bool = False):

    #Plotting
    pos = nx.spring_layout(G, seed=1)  # Seed for reproducible layout
    options = {"edge_color":"k", "node_size": 10, "linewidths": 0, "width": 0.1}
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
    if save_figure:
        fig.savefig(filename, dpi=300, transparent=True)
    else:
        plt.show()

def output_playlist(filename: str, path: List[int], files: List[str]):
    # save playlist
    play_list = []
    print("Mood Playlist Output:")
    for node in path:
        song = basename(files[int(node)])
        play_list.append(song)
        
        print(song)
    
    np.save(filename, play_list)

    print()

def run_path_plotter(file_folder:str, k_hops: int = 10, start_tag: str = 'Mellow', end_tag:str = 'party', force_compute: bool = False):
    path = get_dir_root(file_folder)
    # read in data
    dir_graph_results = path["graph"]

    if force_compute: 
        compute_cosine_sim(file_folder)
        create_cos_graph(file_folder)
    G, path, path_edges, files = calc_path(file_folder, k_hops, start_tag, end_tag)
    plot_graph(G, path_edges, os.path.join(dir_graph_results, f"{start_tag}_to_{end_tag}_spring_layout"), save_figure=True)
    output_playlist(os.path.join(dir_graph_results, f"{start_tag}_to_{end_tag}_play_list"), path, files)
    