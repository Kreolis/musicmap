import pickle
from os.path import dirname
import numpy as np
import scipy
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt

# get colors
colors = plt.get_cmap("gist_ncar")

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

principal_components = np.load(dirname(file_path) + "/principal_feature_components.npy")

top_tags = set(np.argmax(feature_array, axis=1))
num_diff_top_tags = len(top_tags)

# plot
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Principal Component - 1',fontsize=12)
ax.set_ylabel('Principal Component - 2',fontsize=12)
ax.set_title("Principal Component Analysis of music library",fontsize=12)
for i, song in enumerate(songs):
    top_tag = np.argmax(feature_array[i,:])
    ax.scatter(principal_components[i,0], principal_components[i,1], principal_components[i,2], c = colors(top_tag/50), s = 50)
fig.savefig(dirname(file_path) + "/naive_PCA_plot.png")

print()