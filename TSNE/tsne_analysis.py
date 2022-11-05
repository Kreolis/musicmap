from os.path import dirname
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import scipy as sp

# read in data
file_path = "../global_outputs.npy"
songs = np.load(file_path, allow_pickle=True)
num_songs = len(songs)

mean_pool = np.mean(songs[0]["features"]["mean_pool"], axis=0)
#num_features = len(mean_pool)
num_features = len(np.max(songs[0]["taggram"], axis=0))

# create data matrix
feature_array = np.zeros((num_songs, num_features)) 
for i, song in enumerate(range(num_songs)):
    logits = np.mean(songs[i]["taggram"], axis=0)
    print(logits)
    feature_array[i,:] = logits/np.sum(logits)

    max_pool = songs[i]["features"]["max_pool"][-1]
    feature_array[i,:] = max_pool

# TSNE
input_data = StandardScaler().fit_transform(feature_array)
tsne = TSNE(
    n_components=3, 
    learning_rate=200, 
    #early_exaggeration=12, 
    #perplexity=10, 
    verbose=2, 
    #angle=1
)
embedding = tsne.fit_transform(input_data)

np.save(dirname(file_path) + "/tsne_embedding", embedding)

