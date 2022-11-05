import os
import numpy as np
import sys
import matplotlib.pyplot as plt
#from calc import get_files

# read in data
file_path = sys.argv[1]

# get colors
colors = plt.get_cmap("gist_ncar")

# read in data
principal_components = np.load(os.path.join(file_path, "principal_feature_components.npy"))
print("Found ", len(principal_components), " PCAs")
"""
songs = get_files(file_path)
num_songs = len(songs)
num_features = len(songs[0]["tags"])

# create data matrix
feature_array = np.zeros((num_songs, num_features)) 
for i, song in enumerate(range(num_songs)):
    logits = np.mean(songs[i]["taggram"], axis=0)
    feature_array[i,:] = logits/np.sum(logits)


top_tags = set(np.argmax(feature_array, axis=1))
num_diff_top_tags = len(top_tags)
"""
# plot
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, 
    #projection='3d'
    )
ax.set_xlabel('Principal Component - 1',fontsize=12)
ax.set_ylabel('Principal Component - 2',fontsize=12)
#ax.set_ylabel('Principal Component - 3',fontsize=12)
ax.set_title("Principal Component Analysis of music library",fontsize=12)

ax.scatter(principal_components[:,0], 
    principal_components[:,1])
"""
for i, song in enumerate(songs):
    #top_tag = np.argmax(feature_array[i,:])
    ax.scatter(principal_components[:,0], 
    principal_components[:,1], 
    #principal_components[i,2], 
    #c = colors(top_tag/50), 
    s = 50)
#fig.savefig(dirname(file_path) + "/naive_PCA_plot.png")
"""
plt.show()
#print()