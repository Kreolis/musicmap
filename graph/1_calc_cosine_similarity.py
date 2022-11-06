import os
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from utils.misc import get_dir_root

def compute_cosine_sim(file_folder:str):

    path = get_dir_root(file_folder)
    # read in data
    dir_data = path["MSD_tags"]
    dir_out = path["graph"]
    files = sorted(glob(os.path.join(dir_data, "*.npy")))
    num_songs = len(files)

    test = np.load(files[0], allow_pickle=True).item()
    num_features = test["features"]["max_pool"].shape[-1]
    num_logits = len(test["tags"])

    feature_array = {"max":np.zeros((num_songs, num_features)), 
                    "mean":np.zeros((num_songs, num_features))}
    logits_array = np.zeros((num_songs, num_logits))
    top_tags = [None]*num_songs
    for i, file in enumerate(files):
        temp = np.load(file, allow_pickle=True).item()
        feature_array["max"][i, :] = np.max(temp["features"]["max_pool"], axis=0)
        feature_array["mean"][i, :] = np.mean(temp["features"]["mean_pool"], axis=0)
        logits_array[i,:] = np.mean(temp["taggram"], axis=0)
        max_logit = np.argmax(logits_array[i,:])
        top_tags[i] = temp["tags"][max_logit]

        
    np.save(os.path.join(dir_out, "feature_array_max"), feature_array["max"])
    np.save(os.path.join(dir_out, "feature_array_mean"), feature_array["mean"])
    np.save(os.path.join(dir_out, "logits_array"), logits_array)
    np.save(os.path.join(dir_out, "top_tags"), top_tags)

    for key in feature_array:
        # cosine similarity betweeen songs
        cos_sim_songs = np.zeros((num_songs, num_songs)) 
        for i in range(num_songs):
            for j in range(num_songs):
                cos_sim_songs[i,j] = 1 - spatial.distance.cosine(feature_array[key][i,:], feature_array[key][j,:])

        np.save(os.path.join(dir_out, f"cos_sim_songs_{key}"), cos_sim_songs)

        # cosine similarity betweeen tags
        cos_sim_tags = np.zeros((num_features, num_features)) 
        for i in range(num_features):
            for j in range(num_features):
                cos_sim_tags[i,j] = 1 - spatial.distance.cosine(feature_array[key][:,i], feature_array[key][:,j])

        np.save(os.path.join(dir_out, f"cos_sim_tags_{key}"), cos_sim_tags)

        # PLOTTING
        """
        fig, ax = plt.subplots(1)
        ax.set_title("Cosine similarity between songs ",fontsize=12)
        ax.imshow(cos_sim_songs)
        fig.savefig(os.path.join(dir_out, f"cos_sim_songs_{key}.png"))

        fig, ax = plt.subplots(1)
        ax.set_title("Cosine similarity between tags ",fontsize=12)
        ax.imshow(cos_sim_tags)
        fig.savefig(os.path.join(dir_out, f"cos_sim_tags_{key}.png"))
        """
        print()
