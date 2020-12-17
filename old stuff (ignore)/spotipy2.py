import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, session, redirect, url_for, json
from secrets import CLIENT_ID, CLIENT_SECRET
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.secret_key = CLIENT_SECRET

scope = "user-library-read user-top-read"
c = SimpleCache()

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# @app.route("/auth/login")
# def login():
#     sp = spotipy.oauth2.SpotifyClientCredentials
#     app.logger.info(request.args.get("code"))
#     client = spotipy.Spotify(sp.get_access_token(request.args.get("code")))
#     app.logger.info("Currently playing: " + (client.current_user_recently_played()))
#     return "<!DOCTYPE html><html><body>Hello World!</body></html>"
@app.before_first_request
def do_something_only_once():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/", scope=scope))
    c.set("client", sp)
    return sp

@app.route("/", methods=['GET','POST'])
def index():
    sp = c.get("client")
    app.logger.info(sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term'))
    # app.logger.info("Currently playing: " + (sp.current_user_playing_track()))
    # playlists = sp.current_user_saved_tracks()
    user_playlists = sp.user_playlists(sp.current_user()["id"])

    user_albums = sp.current_user_saved_albums()

    app.logger.info("Top artists: " + sp.current_user_top_artists())
    with open('user_playlists.json','w', encoding='utf-8') as output:
        output.write(pretty(user_playlists))

    # app.logger.info("playlists: " + str(playlists))

    app.logger.info(str(sp.current_user()))

    # with open('saved_albums.json','w', encoding='utf-8') as output:
    #     output.write(pretty(user_albums))
    #
    # with open('saved_playlists.json','w', encoding='utf-8') as output:
    #     output.write(pretty(playlists))

    # save_playlist_id = request.form.get('playlist_id')
    # if save_playlist_id:
    #     app.logger.info("playlist id recieved: " + str(save_playlist_id))

    # Checking for searchbar input
    turtle = request.form.get('input')
    app.logger.info("input recieved")
    if turtle:
        # app.logger.info("cheese potato " + str(request.form.get("search-options")))
        type = request.form.get("search-options")
        song_results = sp.search(turtle, type="track")

        # result_dictionary = {}
        # result_dictionary["track"] = sp.search(turtle, type="track")
        # result_dictionary["album"] = sp.search(turtle, type="album")
        # result_dictionary["artist"] = sp.search(turtle, type="artist")
        # result_dictionary["playlists"] = sp.search(turtle, type="playlist")
        # result_dictionary["show"] = sp.search(turtle, type="show")
        # result_dictionary["episode"] = sp.search(turtle, type="episode")
        #
        # with open('search.json','w', encoding='utf-8') as output:
        #     output.write(pretty(song_resuts))

        # with open('song_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["track"]))
        #
        # with open('album_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["album"]))
        #
        # with open('artist_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["artist"]))
        #
        # with open('playlist_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["playlists"]))
        #
        # with open('show_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["show"]))
        #
        # with open('episode_results.json','w', encoding='utf-8') as output:
        #     output.write(pretty(result_dictionary["episode"]))



        # sp.current_user_saved_albums_add(albums=["4GsIzWdN53Kw9DgUKvXuSo"])


        # Going to need to pass search type to template
        return render_template('home.html',user=True,user_playlists=user_playlists,turtle=turtle, response=song_results, user_albums=user_albums)
    else:
        return render_template('home.html',user=True,user_playlists=user_playlists,turtle=turtle, user_albums=user_albums)

@app.route("/save_playlist")
def save():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/", scope=scope))
    playlist_id = request.args.get('pid')
    sp.current_user_saved_albums_add(albums=[playlist_id])
    app.logger.info("Playlist id: " + str(playlist_id))

if __name__ == "__main__":

    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)
