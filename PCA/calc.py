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

# run PCA
input_data = StandardScaler().fit_transform(feature_array)
pca = PCA(n_components=num_features)
principal_components = pca.fit_transform(input_data)

np.save(dirname(file_path) + "/principal_feature_components", principal_components)
np.save(dirname(file_path) + "/explained_variance", pca.explained_variance_)
np.save(dirname(file_path) + "/singular_values", pca.singular_values_)