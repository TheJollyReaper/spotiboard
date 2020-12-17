import spotipy
# from bottle import route, run, request
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, session, redirect, url_for, json, g
from secrets import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)
app.secret_key = CLIENT_SECRET

SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'

@app.route("/")
def index():
    session["client"] = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/", scope=SCOPE)).__dict__
    return redirect('test')

@app.route("/test")
def return_client():
    potato = session.get("client")
    app.logger.info(potato)
    return "<!DOCTYPE html><html><body>potato</body></html>"

if __name__ == "__main__":
    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)
