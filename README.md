# Music Map

Down? Angry? Bored? We can help ease you into a different mood. Musicmap finds the path. 
This small program categorizes your music on your hard drive for later browsing and embeds the genres in an easy-to-navigate visualization and create playlists with a specific mood / genre gradient.

## OVERVIEW:

Many of us have experienced the positive effects that music can have on our mental health, but it is not always easy to find the perfect playlist to improve our mood. Our interactive music map allows users to visualize their music library based on tags related the mood or vibe of the songs, and allows them to create personalized playlists that transition between moods (e.g., from sad to happy songs) to lift them up when they are down. The user can choose a start tag, end tag and number of songs and the created playlist smoothly changes between genres/mood with specidfied direction and number of hops.

Another potential user group is artists and DJs who have a big collection of music. Musicmap automatically embeds the extracted information about the mood, genre, and energy into the metadata of the music file for easy categorization and the Musicmap's interactive visualization provides an interesting analysis  and inspiration tool by displaying __k__ most similar songs to a chosen song.

Musicmap takes advantage of the open-source music-tagging model Musicnn but is in contrast based on the latent embeddings of the model.
Using the embeddings has the advantage of better extracting relations between the songs than using the forced output tags.

This app works on personal, local music libraries, so your playlists can stay completely private. 

![Mellow_to_party_spring_layout](https://user-images.githubusercontent.com/66002874/200176045-65ea2c53-d1eb-4dbc-bc0e-12f64214ccfa.png)

https://user-images.githubusercontent.com/9720532/200154985-32699ad3-6749-4f37-abbd-bf59dd6736b6.mp4


## HOW IT WORKS: 

1. The user specifies a data source. This can be either a local music library or a streaming service like Spotify, Tidal, Soundlcoud or Mixcloud. When using streaming services the user has to first select either the favourite songs or a playlist.
2. The music is then automatically tagged using a pre-trained convolutional neural network [Musicnn](https://github.com/jordipons/musicnn). The program considers a 50-tag vocabulary used in the Million Song Dataset (https://github.com/jongpillee/music_dataset_split/tree/master/MSD_split). 
3. The user can then choose to save the tag information to the songs' metadata. 
4. Using cosine similarity on the latent embeddings we construct a graph network of the music library.
5. The user can then choose to manually explore the graph using the interactive features of the app, extracting neighbor songs of a chosen song.
6. Finally, the user can choose to generate playlists that transition from one area of the graph space to another (e.g., happy to sad). This is done using graph search to create a path of songs of a specified length.

## Usage: the interactive app

To set up the development environment simply enter [`nix-shell`](./shell.nix)
if you're using [Nix](https://github.com/NixOS/nix),
otherwise install `xtensor`, `eigen`, `faiss`, `sqlitecpp`, `sdl2` and `glew`
from [conda-forge](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
or [vcpkg](https://github.com/microsoft/vcpkg).

Fetch the [implot/](./implot) and [imgui/](./imgui) git submodules.

Cf. the next section (preprocessing)
or import the provided [sample data](https://gist.github.com/29ae32af3222950d307883a3d3ad24b5).

```console
$ cmake -B build/ -S . -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
$ cmake --build build/
$ ./build/musicmap
```

The app currently expects the data in `musicmap.db` in the working directory.

## Usage: preprocessing

Clone [musicnn](https://github.com/jordipons/musicnn):

```console
git clone https://github.com/jordipons/musicnn
```

If you have Nix, you can bootstrap a musicnn-friendly environment via [./musicnn-shell.nix](./musicnn-shell.nix).

Install the editable library:

```bash
pip install -e musicnn/
```

If you haven't got Nix yet, you'll have to patch the outdated dependecies in
musicnn so that its setup.py last lines look like that:

```python
install_requires=['librosa',
                'tensorflow>=1.14',
                'numpy']
```


...then install the python3 environment requirements with the [Pipfile](./Pipfile) as a reference:

```bash
pipenv shell
```

Run musicmap.
It will create the sidecar files with the model data and automatically feed that into the route analysis.

```bash
python3 musicmap.py -p <PATH_TO_MP3_FOLDER>
```

```bash
python3 musicmap.py --help
```

Export the pre-computed features and 2D embeddings
via [not-npys-to-sqlite.py](./not-npys-to-sqlite.py)
via [vic-graph-dict-to-sqlite.py](./vic-graph-dict-to-sqlite.py)


## Roadmap

- [x] Figure out how to extract per-song "latent codes" via some learnable model.
  Done via [`musicnn.extractor(..., extract_features=True)`](https://github.com/jordipons/musicnn/). 
  We use the `max_pool` output of the model, which is a (time-indexed) sequence of 753-dimensional vectors.
  We reduce it to a single 753-vector via max pooling.
- [x] Visually 2D/3D embeddings of the latent codes: PCA, tSNE. We've tried representing our song collection as a fully-connected graph with similarity-weighted edges and embedding that in 2D/3D using [networkx](https://networkx.org/). We can export these pre-computed layouts to use with our proof-of-concept interactive app.
- [x] Playlist construction: use the weighted graph interpretation to sample paths between two selected points. For instance, use that to find a "smooth" transition from "sad" songs to "cheerful" music. One can control the tradeoff between the playlist size and the "smoothness". Proof-of-concept in python, via `networkx`.
- [x] App Proof-of-Concept
    - [x] Display the song collection as a scattering of points on a plane: start with fake (randomly generated data
    - [x] Use pre-computed 2D coordinates stored in an sqlite file
    - [x] Ctrl-click on a blob to query its $K$ nearest songs (fixed $K$). Display the selected songs in a list
    - [ ] Song details on hover
    - [ ] Path sampling tool: select a song-origin and a song-destination to get a playlist connecting the two
    - [ ] Incremental and/or external PCA instead of pre-computed coordinates
    - [ ] Export the encoder model (openvino/ONNX) to be used directly in the app.
    - [ ] "Add song" functionality (prerequisite: model export)
    - [ ] A language model with the same latent space as the audio encoder, to
      accomodate song search via text prompts.
    - [ ] Scaling: display "collapsed" blobs instead of individual songs until
      the user zooms in
    - [ ] Static builds
- [x] Junction. Submit.
