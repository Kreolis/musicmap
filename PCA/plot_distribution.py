import numpy as np
import os, sys
import matplotlib.pyplot as plt


# read in data
file_path = sys.argv[1]

# get colors
colors = plt.get_cmap("gist_ncar")

# read in data

singular_values = np.load(os.path.join(file_path,"singular_values.npy"))
explained_variance = np.load(os.path.join(file_path,"explained_variance.npy"))


# plot
plt.figure()
plt.title(f"Distribution of singular values \n Explained varaince: {explained_variance[0]}",fontsize=12)
plt.xlabel('sorted(singular values) ',fontsize=12)
plt.plot(singular_values, c="k")
#plt.savefig(dirname(file_path) + "/component_distribution.png")
plt.show()

print()