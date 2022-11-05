import plotly.express as px
import numpy as np
import os
import pandas as pd


file_path = "../global_outputs.npy"
path = os.path.dirname(file_path)
embedding = np.load(path + "/tsne_embedding.npy")


songs = np.load(file_path, allow_pickle=True)

names = []
top1tag = []

for song in songs:
    base = os.path.basename(song["filename"])
    name = os.path.splitext(base)[0]
    names.append(name)
    top1tag.append(song["toptags"][0])

unique_tags = list(set(top1tag))
print(len(unique_tags))
tag_to_int = {tag: i for i, tag in enumerate(unique_tags)}

tag_ints = [tag_to_int[tag] for tag in top1tag]
print(tag_ints)

plot_3d = True

if plot_3d:
    fig = px.scatter_3d(
        embedding, x=0, y=1, z=2,
        color=tag_ints, 
        text=names
    )
    #fig.update_traces(marker_size=8)
else:
    fig = px.scatter(
    embedding, x=0, y=1,
    color=tag_ints, 
    text=names
)
fig.show()
