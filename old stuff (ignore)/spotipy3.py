import spotipy
# from bottle import route, run, request
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, session, redirect, url_for, json, g
from secrets import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)
app.secret_key = CLIENT_SECRET

SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
# CACHE = '.spotipyoauthcache'

with app.app_context():
    g.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/", scope=SCOPE))


@app.route('/')
@app.before_request
def before_request():

    # g.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/auth_login", scope=SCOPE))
    # # test()
    app.logger.info(g.sp.current_user())
    return "<!DOCTYPE html><html><body>Hello World!</body></html>"
    # if g.sp:
    #     taco()
    #     return "<!DOCTYPE html><html><body>Hello tacos!</body></html>"

# def taco():
#     return redirect(url_for('test'))

@app.route('/auth_login')
def test():
    # app.logger.info(g.sp.current_user())
    return "<!DOCTYPE html><html><body>Hello potatoes!</body></html>"

#     access_token = ""
#
#     token_info = g.sp.get_cached_token()
#
#     if token_info:
#         app.logger.info("found token!")
#         access_token = token_info['access_token']
#     else:
#         url = request.url
#         code = g.sp_oauth.parse_response_code(url)
#         if code:
#             app.logger.info("Found Spotify auth code in Request URL! Trying to get valid access token...")
#             token_info = g.sp_oauth.get_access_token(code)
#             access_token = token_info['access_token']
#
#     if access_token:
#         app.logger.info("Access token available! Trying to get user information...")
#         sp = spotipy.Spotify(access_token)
#         results = sp.current_user()
#         return results
#
#     else:
#         return htmlForLoginButton()
#
# def htmlForLoginButton():
#     auth_url = getSPOauthURI()
#     htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
#     return htmlLoginButton
#
# def getSPOauthURI():
#     auth_url = sp_oauth.get_authorize_url()
#     return auth_url


if __name__ == "__main__":
    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)
