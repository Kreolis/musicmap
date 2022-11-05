from os.path import dirname
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

# read in data
file_path = "/home/oberlav1/scratch/graphics/oberlav1/junction22/global_outputs.npy"
songs = np.load(file_path, allow_pickle=True)
num_songs = len(songs)
num_features = len(songs[0]["tags"])

# create data matrix
feature_array = np.zeros((num_songs, num_features)) 
for i, song in enumerate(range(num_songs)):
    logits = np.mean(songs[i]["taggram"], axis=0)
    feature_array[i,:] = logits/np.sum(logits)

# TSNE
input_data = StandardScaler().fit_transform(feature_array)
tsne = TSNE(n_components=3, learning_rate=200, perplexity=100, verbose=2, angle=0.1)
embedding = tsne.fit_transform(input_data)

np.save(dirname(file_path) + "/tsne_embedding", embedding)

