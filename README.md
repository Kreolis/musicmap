# Music Map

## Pitch

Down? Angry? Bored? We can help ease you into a different mood. Musicmap finds the path. 
This small program categorizes your music on your hard drive for later browsing and embeds the genres in an easy-to-navigate visualization to create mood playlists.
It can use several different algorithms and AI models for music indexing.



https://user-images.githubusercontent.com/9720532/200154985-32699ad3-6749-4f37-abbd-bf59dd6736b6.mp4



## OVERVIEW:

Musicmap is a versatile music library visualization app that is applicable to a variety of audiences. 

Many of us have experienced the positive effects that music can have on our mental health, but it is not always easy to find the perfect playlist to improve our mood. Our interactive music map allows users to visualize their music library based on tags related the mood or vibe of the songs, and allows them to create personalized playlists that transition between moods (e.g., from sad to happy songs) to lift them up when they are down. This app works on personal, local music libraries, so your playlists can stay completely private. 

Another potential user group is artists and DJs who have a big collection of music. A DJ often has new music that they want to categorize and analyze, and using Musicmap's interactive visualization, they can streamline this process. Musicmap automatically embeds the extracted information about the mood, genre, and energy into the metadata of the music file for easy categorization. For artists, it can provide a quick way of getting new inspiration. One can use it either in random mode where it can play and maintain a random mood or genre , or one can specify a mood they want to explore to aid in the creative process.

Musicmap takes advantage of the open-source music-tagging model Musicnn to provide users with an user-friendly, interactive way to explore and organize their personal music libraries, and create personalized playlists that can benefit the user's mental health and creative productivity. 

## HOW IT WORKS: 

1. The user specifies a data source. This can be either a local music library or a streaming service like Spotify, Tidal, Soundlcoud or Mixcloud. When using streaming services the user has to first select either the favourite songs or a playlist.
2. The music is then automatically tagged using a pre-trained convolutional neural network [Musicnn](https://github.com/jordipons/musicnn). The program considers a 50-tag vocabulary used in the Million Song Dataset (https://github.com/jongpillee/music_dataset_split/tree/master/MSD_split). 
3. The user can then choose to save the tag information to the songs' metadata. 
4.  Using a combination of principal component analysis (PCA) and graph search the program will then display the latent tag space of the provided music in 2D and 3D.
5. The user can then choose to manually explore the latent space using the interactive features of the app. 
6. Finally, the user can choose to generate playlists. This is done using graph search to create a path of songs of a specified length. Playlists can be created within a specified graph space, or  can be made  such that the songs transition from one area of the graph space to another (e.g., happy to sad). 

## Usage: the interactive app

To set up the development environment simply enter [`nix-shell`](./shell.nix)
if you're using [Nix](https://github.com/NixOS/nix),
otherwise install `xtensor`, `eigen`, `faiss`, `sqlitecpp`, `sdl2` and `glew`
from [conda-forge](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
or [vcpkg](https://github.com/microsoft/vcpkg).

Fetch the [implot/](./implot) and [imgui/](./imgui) git submodules.

```console
$ cmake -B build/ -S . -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
$ cmake --build build/
$ ./build/musicmap
```

## Usage: preprocessing

Clone [Musicnn](https://github.com/jordipons/musicnn) as a subfolder in this repository. 

```bash
git clone https://github.com/jordipons/musicnn
```

Install the python3 environment requirements from the Pipfile.
Start the enviroment:

```bash
pipenv shell
```

Run musicmap. It will create the sidecar files with the model data and automatically feed that into the route analysis.

```bash
python3 musicmap.py -p <PATH_TO_MP3_FOLDER>
```

```bash
python3 musicmap.py --help
```

Export the pre-computed features and 2D embeddings
via [not-npys-to-sqlite.py](./not-npys-to-sqlite.py)
via [vic-graph-dict-to-sqlite.py](./vic-graph-dict-to-sqlite.py)
