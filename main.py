"""
Note: I used Mohith Subbarao's app Moodtape as a reference. Great app Mohith!
GitHub link: https://github.com/mohithsubbarao/moodtape
Medium link: https://medium.com/@mohithsubbarao/moodtape-using-spotify-api-to-create-mood-generated-playlists-6e1244c70892
"""

import sys
import spotipy
import spotipy.util as util
from flask import Flask, flash, redirect, render_template, request, session, abort
from functions import authenticate_spotify, get_top_artists, get_top_artists_tracks, get_top_tracks, create_profile, compare_to_candidates
from keys import *

scope = 'user-library-read user-top-read user-follow-read'

# username = "1213054860"
# Anna: spotify:user:1240918025
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
# 	print('Username required!')
# 	print('Usage: %s username' % (sys.argv[0],))
# 	sys.exit()

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('input.html')


@app.route("/", methods=['POST'])
def run_app():
	username = request.form['username']
	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
	spotify_auth = authenticate_spotify(token)
	top_artists = get_top_artists(spotify_auth)
	top_artists_tracks = get_top_artists_tracks(spotify_auth, top_artists)
	top_tracks = get_top_tracks(spotify_auth)

	all_tracks = top_artists_tracks + top_tracks
	user_profile = create_profile(spotify_auth, 'user', all_tracks, top_artists)

	result = compare_to_candidates(spotify_auth, user_profile)
	top_candidate = result[0][0]
	# image_path = 'candidate-pictures/' + top_candidate + '.jpg'
	image_path = result[0][2]
	print(result)
	print(top_candidate)
	print(image_path)
	return render_template('result.html', result=result, candidate=top_candidate, image=image_path)

if __name__ == "__main__":

	app.run(port=8888)