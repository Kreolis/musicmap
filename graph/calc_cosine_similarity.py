import pickle
from os.path import dirname
import numpy as np
from scipy import spatial

# read in data
file_path = "/home/oberlav1/scratch/graphics/oberlav1/junction22/global_outputs.npy"
songs = np.load(file_path, allow_pickle=True)
num_songs = len(songs)
num_features = len(songs[0]["tags"])

# create data matrix
cosine_sim_matrix = np.zeros((num_songs, num_songs)) 
for i in range(num_songs):
    for j in range(num_songs):
        logits_i = np.mean(songs[i]["taggram"], axis=0)
        logits_j = np.mean(songs[j]["taggram"], axis=0)
        cosine_sim = 1 - spatial.distance.cosine(logits_i, logits_j)
        cosine_sim_matrix[i,j] = cosine_sim

np.save(dirname(file_path) + "/cosine_sim_matrix", cosine_sim_matrix)

print()
