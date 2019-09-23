import sys
import spotipy
import spotipy.util as util
import random

def get_candidate(sp, candidate):
	playlist_uris = {}

	playlist_uris['Donald Trump'] = 'spotify:playlist:4i267YUdtdfLQyhS13vjq0'
	playlist_uris['Joe Biden'] = 'spotify:playlist:6o44CNBofHqLyikI5VVyZ7'
	playlist_uris['Pete Buttigieg'] = 'spotify:playlist:6N6n8nK4jHdi7SsaDFYa8Q'
	playlist_uris['Julian Castro'] = 'spotify:playlist:2NY2xZKejmpQXiz7lkWUlI'
	playlist_uris['Cory Booker'] = 'spotify:playlist:0AgCqEz1l2o2AAMx0CEm72'
	playlist_uris['Bernie Sanders'] = 'spotify:playlist:5snNr8XEYZBA3AsCoNw4lo'
	playlist_uris['Kirsten Gillibrand'] = 'spotify:playlist:4LlmxLNPVApnBFjPdiPI0X'
	playlist_uris['Elizabeth Warren'] = 'spotify:playlist:6YRWneVEDsSEiQOJ5e7R3Z'
	playlist_uris["Beto O'Rourke"] = 'spotify:playlist:0Ztf87HOfRF3XMy9AGu4Dm'
	playlist_uris['Kamala Harris'] = 'spotify:playlist:3I8VI6fZMRvIyRHmqc3qda'
	playlist_uris['Andrew Yang'] = 'spotify:playlist:6DB8wXUA71Q0xqMs23y0Fe'
	
	playlist = sp.user_playlist('1213054860', playlist_uris[candidate])

	tracks = playlist['tracks']['items']

	image = playlist['images'][0]['url']

	track_uris = []
	artist_uris = []

	for track in tracks:
		track_uris.append(track['track']['uri'])
		artists = track['track']['artists']
		for artist in artists:
			artist_uris.append(artist['uri'])
	
	return track_uris, artist_uris, image
