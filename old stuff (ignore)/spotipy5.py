import spotipy, sys
# from bottle import route, run, request
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, session, redirect, url_for, json
from secrets import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)
app.secret_key = CLIENT_SECRET

SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
scope = "user-library-read user-read-recently-played"

@app.route("/")
def index():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/auth/login", scope=scope))
    app.logger.info(sp.current_user())
    return "<!DOCTYPE html><html><body>cheese</body></html>"

@app.route("/auth/login")
def main():
    verification_code = request.args.get("code")

    app.logger.info(verification_code)
    app.logger.info(sp.current_user())
    app.logger.info(sp.current_user_recently_played())
    return "<!DOCTYPE html><html><body>potato</body></html>"
# @app.route("/auth/login")
# def send_back():
#     return "<!DOCTYPE html><html><body>potato</body></html>"

if __name__ == "__main__":



    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)
