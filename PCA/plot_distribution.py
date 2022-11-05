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
singular_values = np.load(dirname(file_path) + "/singular_values.npy")
explained_variance = np.load(dirname(file_path) + "/explained_variance.npy")


# plot
plt.figure()
plt.title(f"Distribution of singular values \n Explained varaince: {explained_variance[0]}",fontsize=12)
plt.xlabel('sorted(singular values) ',fontsize=12)
plt.plot(singular_values, c="k")
plt.savefig(dirname(file_path) + "/component_distribution.png")

print()