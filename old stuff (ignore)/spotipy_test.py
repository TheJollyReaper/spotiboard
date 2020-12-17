# import spotipy, json
# from spotipy.oauth2 import SpotifyClientCredentials
#
# def pretty(obj):
#     return json.dumps(obj, sort_keys=True, indent=2)
#
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="a9bd404bbb5d4bc3bd329e3c449044f0", client_secret="8d67360c915a44b9a41a6b3d86e2c561"))
#
# print(pretty(spotify.search("potato", type='track')))

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

from secrets import CLIENT_ID, CLIENT_SECRET
GRANT_TYPE = 'authorization_code'

app.secret_key = CLIENT_SECRET

@app.route("/")
def index():
    logged_in = False

    sp = "potato"

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        app.logger.info(idx, track['artists'][0]['name'], " – ", track['name'])


    return redirect(url_for('index', sp=sp))
    # if sp is not None:
    #     sp = session['client']
    #     results = sp.current_user_saved_tracks()
    #     for idx, item in enumerate(results['items']):
    #         track = item['track']
    #         app.logger.info(idx, track['artists'][0]['name'], " – ", track['name'])
    #     return render_template('home.html')
    # else:
    #     sp = get_client()
    #     return redirect(url_for('index', sp=sp))

@app.route("/login")
def authorize():
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENT_ID", client_secret="CLIENT_SECRET", redirect_uri="http://localhost:8080", scope=scope))

    # return render_template('home.html')

# def get_client():
#
#     return sp

if __name__ == "__main__":
    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])
