import sys, os, tqdm
from halo import Halo
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# read in data
file_path = sys.argv[1]



def get_files(file_path):
    """Collecting all files to be processed"""
    songs = []

    print("Loading files")
    for root, dirs, files in os.walk(file_path):
        print("Got", len(files), "files")
    
        for file in tqdm.tqdm(files):
            if file.endswith(".npy"):
                try:
                    data = np.load(os.path.join(root, file), allow_pickle=True).item()
                    data.pop("features", None)
                
                    songs.append(data)
                except EOFError:
                    print("skipping ", file)
        break

    return songs

songs = get_files(file_path)
#songs = np.load(file_path, allow_pickle=True)
num_songs = len(songs)
num_features = len(songs[0]["tags"])

spinner = Halo(text='preparing data for PCA', spinner='dots')
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want

# create data matrix
feature_array = np.zeros((num_songs, num_features)) 
for i, song in enumerate(range(num_songs)):
    logits = np.mean(songs[i]["taggram"], axis=0)
    feature_array[i,:] = logits/np.sum(logits)

spinner.stop()

spinner = Halo(text='running PCA', spinner='dots')
spinner.start()
# run PCA
input_data = StandardScaler().fit_transform(feature_array)
pca = PCA(n_components=num_features)
principal_components = pca.fit_transform(input_data)

spinner.stop()

spinner = Halo(text='saving PCA data to files', spinner='dots')
spinner.start()

np.save(os.path.join(file_path, "principal_feature_components"), principal_components)
np.save(os.path.join(file_path, "explained_variance"), pca.explained_variance_)
np.save(os.path.join(file_path, "singular_values"), pca.singular_values_)

spinner.stop()

print("PCA files saved")
