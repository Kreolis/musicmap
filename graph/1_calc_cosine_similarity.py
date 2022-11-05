from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from utils.misc import get_dir_root

path = get_dir_root()
# read in data
dir_data = path["MSD_tags"]
dir_out = path["graph"]
files = sorted(glob(dir_data + "/*.npy"))
num_songs = len(files)

test = np.load(files[0], allow_pickle=True).item()
num_features = test["features"]["max_pool"].shape[-1]

feature_array = np.zeros((num_songs, num_features))
top_tags = [None]*num_songs
for i, file in enumerate(files):
    temp = np.load(file, allow_pickle=True).item()
    feature_array[i, :] = np.mean(temp["features"]["max_pool"], axis=0)
    logits = np.mean(temp["taggram"], axis=0)
    max_logit = np.argmax(logits)
    top_tags[i] = temp["tags"][max_logit]

np.save(dir_out + "/feature_array", feature_array)
np.save(dir_out + "/top_tags", top_tags)

# cosine similarity betweeen songs
cos_sim_songs = np.zeros((num_songs, num_songs)) 
for i in range(num_songs):
    for j in range(num_songs):
        cos_sim_songs[i,j] = 1 - spatial.distance.cosine(feature_array[i,:], feature_array[j,:])

np.save(dir_out + "/cos_sim_songs", cos_sim_songs)

# cosine similarity betweeen tags
cos_sim_tags = np.zeros((num_features, num_features)) 
for i in range(num_features):
    for j in range(num_features):
        cos_sim_tags[i,j] = 1 - spatial.distance.cosine(feature_array[:,i], feature_array[:,j])

np.save(dir_out + "/cos_sim_tags", cos_sim_tags)

# PLOTTING
fig, ax = plt.subplots(1)
ax.set_title("Cosine similarity between songs ",fontsize=12)
ax.imshow(cos_sim_songs)
fig.savefig(dir_out + "/cos_sim_songs.png")

fig, ax = plt.subplots(1)
ax.set_title("Cosine similarity between tags ",fontsize=12)
ax.imshow(cos_sim_tags)
fig.savefig(dir_out + "/cos_sim_tags.png")

print()
