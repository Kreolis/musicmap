# Music Map

## Pitch

This small program categorizes your music on your hard drive for later browsing and embeds the genres in an easy-to-navigate visualization to create mood playlists.
It can use several different algorithms and AI models for music indexing.

## Audience

This app can serve several different audiences.

One is artists and DJs with a big collection of music or new music.
A DJ often has new music he has to categorize and analyze.
Here the app can help to fasten up the music selection process.
It can detect genre, mood and energy of a song.
The information can automatically be embedded into the meta data of the music file.

For artists, it can provide a quick way of getting new inspiration.
Similar songs a grouped together.
One can use it either in random mode where it can play a random mood or genre and stay with it.
Or selecting a certain mood one wants to explore for a new creation to aid in the production process of it.

For even quicker interaction the audio from a microphone can be analyzed and the program will guide the user to similar sounding tracks in the collection.
The program can also automatically create a playlist for a selected mood.
To help the user get into a happier state it starts of with a sad mood and gradually makes the songs in the playlist happier.

By providing the lyrics to a song another model can be used to explore the music category space by filtering it with text prompts (DALL-E2 style) additionally to the mood and genre.


## Functionallity

```flow
st=>start: music files
op1=>operation: mood and tag analysis
cond1=>condition: save to meta data?
op2=>operation: save tag to meta data
op3=>operation: display latent space
cond2=>condition: manual exploring?
op4=>operation: user explores
op5=>operation: collect similar music
e=>end: output similar music as playlist

st->op1->cond1->op2
cond1(yes)->op3
cond1(no)->op2
op2->op3->cond2
cond2(yes)->op5
cond2(no)->op4
op4->op5->e
```

The user specifies a data source.
This can be either a local music library or a streaming service like Spotify, Tidal, Soundlcoud or Mixcloud.
When using streaming services the user has to first select either the favorite songs or a playlist.

The program will analyses the music using [Musicnn](https://github.com/jordipons/musicnn).
It does not use any cloud services for the analysis.
[Other tagging algorithms](https://github.com/minzwon/sota-music-tagging-models) can be used.
Based on work by [Won et al. 2020](https://arxiv.org/abs/2006.00751), simple short-chunk CNN models perform the best for music-tagging and have the best generalization abilities.
Musicnn, which takes into consideration intuition from the music domain, performs well for small data samples but does not generalize well to larger datasets.
Song-level or long chunk-level trained models do not perform as well for music-tagging applications.

The tags and intermediate analysis results. 
By using a combination of principal component analysis (PCA) and t-distributed stochastic neighbor embedding (t-SNE) the program can display the latent tag space of the provided music in 2D and 3D.
