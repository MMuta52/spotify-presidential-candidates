<<<<<<< HEAD
# Spotify Presidential Candidates

The New York Times published an [article](https://www.nytimes.com/interactive/2019/08/19/us/politics/presidential-campaign-songs-playlists.html?smtyp=cur&smid=tw-nytimes) analyzing the music played at campaign rallies of the 2020 United States Presidential candidates. The article is really interesting and the graphics are very well done---definitely give it a read!

Using the playlists that they published for each candidate, this app compares your Spotify listening history to each candidate and tells you whose campaign music is most similar to your music.

# Usage
- Explain that didn't want to host on webpage
- Explain that need to email me for keys
- Put key file into folder
- Make sure using Python 3
- (insert how to pip install all dependencies from requirements.txt, recommend a venv)
- Go to directory in terminal and run command "python main.py"
- Will likely ask u to log in, then will throw a 404 not found page. The terminal should say something along the lines of "paste the URL you were redirected to in here". Copy/paste the url from the 404 not found page into the terminal
- In web browser, type "localhost:8080"
- See results!

# The Process

With no real metric for evaluating the music someone listens to, I turned to the [Spotify API](https://developer.spotify.com/documentation/web-api/) for ideas. I eventually settled on the following implementation:

1. I create a **listening profile** for a user as follows:
	- **Top artists:** I compile the user's top artists using [this endpoint](https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/). I consider top artists over short-term (the past 4 weeks), medium-term (the past 6 months), and long-term (the past several years.)
	- **Genres:** I find the most commonly occurring genres across these artists and store them weighted by frequency.
	- **Top tracks:** I compile the user's top tracks using [this endpoint](https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/). I also add the top 10 tracks of each of the user's top artists using [this endpoint](https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/). From here, I use [this endpoint](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/) to get **audio features** for each track and average across them to build a picture of the type of music based on things like danceability, energy, and tempo.

 2. I follow the same procedure to create a listening profile for each of the presidential candidates based on their campaign rally playlists.

 3. I compare the user profile to each candidate. My procedure for comparing two profiles is as follows:
	 - Compute the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) between the two users' average audio features from their top tracks. Call this **audio_dist**.
	 - Compare the lists of top artists and compute what proportion of artists overlap. Call this **artist_overlap**.
	 - Compare the lists of genres and compute what proportion of genres overlap. I only include genres that apply to more than 10% of a user's artists. Call this **genre_overlap**.
	 - I define the difference between two profiles as:
	 >**audio_dist** x (1- **artist_overlap**)<sup>2</sup> x (1-**genre_overlap**)

I square the artist component because I felt that listening to the same artist as someone is more significant than simply listening to music from the same genre or with similar audio features.

4. Finally, I rank each candidate based on their distance from the user as calculated above.

# File Structure

# Dependencies

[Keras](https://keras.io) and [Tensorflow](https://www.tensorflow.org) - Neural network training
[Numpy](https://numpy.org) - Math
[Matplotlib](https://matplotlib.org) - Displaying images

# Future Work
Mention instead of averaging across musical features, use clustering to learn (machine learning!!) several distinct types of music that the person likes and look for each one individually rather than averaging across and potentially losing information/creating a noisy, meaningless profile.

mention add andrew yang, maybe obama

maybe will host on webpage for public use or explore other options to make usable by other people
=======
# spotify-presidential-candidates
>>>>>>> 058c47bf681f623d9f26fe883f586b197ccccab5
