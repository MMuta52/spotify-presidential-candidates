import spotipy
import spotipy.util as util
import pandas as pd
import numpy as np
from collections import Counter
from candidates import get_candidate

# Step 1: Authenticate
def authenticate_spotify(token):
	"""
	Authenticate for permission to access user's Spotify information
	"""
	print('...connecting to Spotify')
	sp = spotipy.Spotify(auth=token)
	return sp

# Step 2. Creating a list of your favorite artists

def get_top_artists(sp):
	"""
	Get top artists for the user
	"""
	print('...getting user top artists')
	top_artists_name = []
	top_artists_uri = []

	# Consider short term (last 4 weeks), medium term (last 6 months), and long term (several years) listening habits
	ranges = ['short_term', 'medium_term', 'long_term']

	for r in ranges:
		artist_results = sp.current_user_top_artists(limit=30, time_range= r)
		top_artists_data = artist_results['items']

		for artist_data in top_artists_data:
			if artist_data["uri"] not in top_artists_uri:		
				top_artists_name.append(artist_data['name'])
				top_artists_uri.append(artist_data['uri'])

	return top_artists_uri

# Step 3. Get the top 10 tracks of each artist

def get_top_artists_tracks(sp, top_artists_uri):
	"""
	Get top 10 tracks of a given artist
	"""
	print("...getting artists top tracks")
	top_tracks_uri = []
	for artist in top_artists_uri:
		artist_tracks_results = sp.artist_top_tracks(artist)
		artist_tracks_data = artist_tracks_results['tracks']
		for track_data in artist_tracks_data:
			top_tracks_uri.append(track_data['uri'])

	return top_tracks_uri

# Step 4. Get user's top tracks
def get_top_tracks(sp):
	"""
	Get user's top tracks
	"""
	print("...getting user's top tracks")
	top_tracks_name = []
	top_tracks_uri = []

	# Just get top 10 tracks for short term, don't want to be skewed by recent listening
	short_results = sp.current_user_top_tracks(limit=15, time_range='short_term')
	top_tracks_data = short_results['items']

	for track_data in top_tracks_data:
		if track_data['uri'] not in top_tracks_uri:
			top_tracks_name.append(track_data['name'])
			top_tracks_uri.append(track_data['uri'])

	# Now get all top tracks for medium and long term
	for r in ['medium_term', 'long_term']:
		track_results = sp.current_user_top_tracks(limit=50, time_range=r)
		top_tracks_data = track_results['items']

		# Loop to allow for a limit of more than 50
		while track_results['next']:
			track_results = sp.next(track_results)
			top_tracks_data.extend(track_results['items'])

		for track_data in top_tracks_data:
			if track_data['uri'] not in top_tracks_uri:
				top_tracks_name.append(track_data['name'])
				top_tracks_uri.append(track_data['uri'])

	return top_tracks_uri


# Step 5. Create profile of a user given their top tracks and artists
def get_user_genres(sp, artist_uri_list):
	"""
	Create dictionary of most common genres among a list of artists
	"""

	# Get artists (have to use this silly loop because Spotify only allows requesting 50 artists at a time)
	artists = []
	i = 0
	while i < len(artist_uri_list):
		artists.extend(sp.artists(artist_uri_list[i:i+50])['artists'])
		i += 50

	# artists = sp.artists(artist_uri_list)['artists']
	genres = []
	for artist in artists:
		genres.extend(artist['genres'])

	# Map genre to number of occurences of that genre
	genre_count = Counter(genres)
	# Now map genre to what proportion of the genres it makes up
	genre_proportion = {k:(v / len(artist_uri_list)) for k, v in genre_count.items()}

	return genre_proportion


def create_profile(sp, name, tracks, artists, image=None):
	"""
	Create a profile of a given user's listening history given top tracks and artists
	"""
	print('...generating profile for ' + name)

	profile = {}
	profile['danceability'] = 0
	profile['energy'] = 0
	profile['instrumentalness'] = 0
	profile['liveness'] = 0
	profile['loudness'] = 0
	profile['speechiness'] = 0
	profile['valence'] = 0

	tracks_features = []
	for i in range(0,len(tracks),50):
		tracks_features.extend(sp.audio_features(tracks[i:i+50]))

	# Compute average features
	for track in tracks_features:
		profile['danceability'] += track['danceability']
		profile['energy'] += track['energy']
		profile['instrumentalness'] += track['instrumentalness']
		profile['liveness'] += track['liveness']
		profile['loudness'] += track['loudness'] / -60 # This feature comes on a scale of -60 to 0
		profile['speechiness'] += track['speechiness']
		profile['valence'] += track['valence']

	profile = {k:(v / len(tracks)) for k, v in profile.items()}
	profile['name'] = name

	genres = get_user_genres(sp, artists)
	profile['genres'] = genres

	profile['artists'] = artists
	profile['image'] = image

	return pd.Series(profile)

# Step 6. Create dataframe of candidate profiles
def candidate_profiles(sp):
	"""
	Compile candidate profiles into one dataframe
	"""
	candidate_df = pd.DataFrame(columns=['name', 'image', 'danceability','energy','instrumentalness','liveness','loudness','speechiness','valence'])
	candidates = ['Donald Trump', 'Joe Biden', 'Pete Buttigieg', 'Julian Castro', 'Cory Booker', 'Bernie Sanders', 'Kirsten Gillibrand', 'Elizabeth Warren', "Beto O'Rourke", 'Kamala Harris', 'Andrew Yang']
	for candidate in candidates:
		tracks, artists, image = get_candidate(sp, candidate)
		profile = create_profile(sp, candidate, tracks, artists, image=image)
		candidate_df = candidate_df.append(profile, ignore_index=True)
	
	return candidate_df

# Step 7. Compare profiles of two users

def compare_artists(artists_a, artists_b):
	"""
	Measure proportion of common artists between two profiles
	"""
	common_artists = 0
	if len(artists_a) > len(artists_b):
		for b in artists_b:
			if b in artists_a:
				common_artists += 1

		return common_artists / len(artists_b)

	else:
		for a in artists_a:
			if a in artists_b:
				common_artists += 1

		return common_artists / len(artists_a)

def compare_genres(genres_a, genres_b):
	"""
	Measure proportion of common genres between two profiles
	"""
	# Get all genres that make up higher than 10% of the user's genres
	top_genres_a = []
	top_genres_b = []
	for genre in genres_a:
		if genres_a[genre] > 0.1:
			top_genres_a.append(genre)

	for genre in genres_b:
		if genres_b[genre] > 0.1:
			top_genres_b.append(genre)

	# Count number of common genres and divide by total number of genres
	common_genres = 0
	if len(top_genres_a) > len(top_genres_b):
		for b in top_genres_b:
			if b in top_genres_a:
				common_genres += 1

		return common_genres / len(top_genres_b)

	else:
		for a in top_genres_a:
			if a in top_genres_b:
				common_genres += 1

		return common_genres / len(top_genres_a)


def compare_profiles(profile_a, profile_b):
	"""
	Compare profiles of two users
	"""

	features_a = profile_a.drop(['name', 'artists', 'genres'])
	features_b = profile_b.drop(['name', 'artists', 'genres'])
	
	feature_diff = np.sqrt((features_a - features_b).pow(2).sum(0)) # Euclidean distance
	artist_diff = 1 - compare_artists(profile_a['artists'], profile_b['artists']) # Inverse proportion of overlap
	genre_diff = 1 - compare_genres(profile_a['genres'], profile_b['genres']) # Inverse proportion of overlap

	diff = feature_diff * artist_diff**2 * genre_diff # Square artists component to heavily weigh artist simiarlities

	return diff


def compare_to_candidates(sp, user_profile):
	"""
	Compare a given profile to the candidates and return result of comparison to each candidate
	"""
	candidate_df = candidate_profiles(sp)
	results = []

	for __, candidate in candidate_df.iterrows():

	# for candidate in candidate_df:
		diff = compare_profiles(user_profile, candidate.squeeze())
		results.append((candidate['name'], diff, candidate['image']))

	return sorted(results, key = lambda x:x[1])




