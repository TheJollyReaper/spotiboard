import urllib.request, urllib.error, urllib.parse, json, requests
from flask import Flask, render_template, request, session, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import CLIENT_ID, CLIENT_SECRET, LYRICS_KEY

app = Flask(__name__)


GRANT_TYPE = 'authorization_code'

app.secret_key = CLIENT_SECRET

def retrieve_lyrics(artist, track):
    artist = artist
    track = track
    params = {}
    params["apikey"] = LYRICS_KEY
    baseurl = "https://orion.apiseeds.com/api/music/lyric/{artist}/{track}".format(artist=artist, track=track)
    app.logger.info("Lyrics URL: " + str(baseurl))
    url = baseurl + "?" + urllib.parse.urlencode(params)
    url = baseurl + "?" + urllib.parse.urlencode(params)
    try:
        lyrics_response = requests.get(url).json()
        return lyrics_response
    except:
        return "Lyrics not found :("

def spotifyurlfetch(url,access_token,params=None):
    headers = {'Authorization': 'Bearer '+access_token}
    req = urllib.request.Request(
        url = url,
        data = params,
        headers = headers
    )
    app.logger.info("banana banana banana" + str(req))
    response = urllib.request.urlopen(req)
    app.logger.info(response)
    return response.read()

@app.route("/save_album")
def save():
    sp = spotipy.Spotify(session["access_token"])
    id = request.args.get('id')
    app.logger.info(id)
    sp.current_user_saved_albums_add([id])

# @app.route("/save_playlist")
# def follow_playlist():
#     # "1zN85Ep8w2JORfCe0RHLDP"
#     id = request.args.get("id")
#     url = "https://api.spotify.com/v1/playlists/{id}/followers".format(id=id)
#
#     app.logger.info(url)
#     headers = {
#         'Authorization': 'Bearer '+access_token,
#         'Content-Type': 'application/json'
#         }

    # req = urllib.request.Request(
    #     url = url,
    #     headers = headers,
    #     method = "PUT"
    # )
    # response = requests.put(url, headers=headers)
    # app.logger.info("response is: " + str(response))

def safeGet(url, headers=None):
    try:
        return requests.get(url, headers=headers).json()
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def search(input, token):
    # url = "https://api.spotify.com/v1/search"
    # response = json.loads(spotifyurlfetch(url,session["access_token"]))
    app.logger.info(token)
    headers = {
        "Authorization": str("Bearer " + token)
    }

    endpoint = "https://api.spotify.com/v1/search"
    data = urllib.parse.urlencode({"q": input, "type": "track"})
    request_url = str(endpoint + "?" + data)
    app.logger.info(request_url)
    return safeGet(request_url, headers)

@app.route("/", methods=['GET','POST'])
def index():
    if 'user_id' in session:
        user = session["user_id"]
        sp = spotipy.Spotify(session["access_token"])
    else:
        user = None

    if user != None:
        # refresh token eventually

        app.logger.info("DEVICES: " + str(sp.devices()))

        user_playlists = {}
        user_playlists_response = sp.user_playlists(sp.current_user()["id"])
        for playlist in user_playlists_response["items"]:
            user_playlists[str(playlist["name"])] = {"info": sp.playlist_items(playlist["id"])}


        user_albums = sp.current_user_saved_albums()
        app.logger.info("recently played: " + str(sp.current_user_recently_played()))
        # app.logger.info("currently playing: " + str(sp.current_user_playing_track()))
    else:
        user_playlists = None
        user_albums = None

    app.logger.info(request.form.get('input'))
    turtle = request.form.get('input')

    # app.logger.info("testing saving playlist" + str(follow_playlist(session["access_token"])))


    # follow_playlist(session["access_token"], "1zN85Ep8w2JORfCe0RHLDP")

    if turtle:
        search_type = request.form.get('search-options')
        # app.logger.info(session["access_token"])
        # song_results={

        # song_results = search(turtle, session["access_token"])
        if search_type == "track":
            tracks_cleaned = {}
            song_results = sp.search(q=turtle, type="track")
            for item in song_results["tracks"]["items"]:
                # tracks[item["album"]["name"]] = sp.album_tracks(item["album"]["id"])
                track_list = sp.album_tracks(item["album"]["id"])

                for track in track_list["items"]:
                    if turtle.lower() in track["name"].lower():
                        # app.logger.info(track["artists"][0]["name"])
                        tracks_cleaned[track["name"]] = {"artist": track["artists"][0]["name"], "uri":track["uri"]}
            return render_template('home.html',user=True,user_playlists=user_playlists,turtle=turtle, response=tracks_cleaned, user_albums=user_albums)

        if search_type == "album":
            album_search_results = {}
            album_results = sp.search(q=turtle, type="album")
            for album in album_results["albums"]["items"]:
                track_list = sp.album_tracks(album["id"])
                # app.logger.info(album["name"])
                # album_search_results[album["name"]] = {}
                tracklist = {}
                for track in track_list["items"]:
                    # app.logger.info(track)
                    # album_search_results[track["name"]] = "potato"
                    tracklist[track["name"]] = {"artist": track["artists"][0]["name"], "uri":track["uri"], "name":track["name"]}
                    # album_search_results[album["name"]][track["name"]] = track["name"]
                # album_search_results[album["name"]] = sp.album_tracks(album["id"])
                album_search_results[album["name"]] = {"tracks":tracklist, "id":album["id"]}
            return render_template('home.html',user=True,user_playlists=user_playlists,turtle=turtle, user_albums=user_albums, search_albums=album_search_results)

            # app.logger.info(sp.album_tracks(item["album"]["id"]))
            # for album in item["album"]:
            #     tracks[album["name"]]= album["id"]
            #     # tracks = sp.album_tracks(id)

        # app.logger.info(song_results)
        return render_template('home.html',user=True,user_playlists=user_playlists,turtle=turtle, user_albums=user_albums)

    # I wanted to use 'input' as the variable, but that seems to break the code
    # So I settled for turtle
    else:
        return render_template('home.html',user=user,user_playlists=user_playlists,turtle=turtle, user_albums=user_albums)

### this handler will handle our authorization requests
@app.route("/auth/login")
def login_handler():
    # after  login; redirected here
    # did we get a successful login back?
    args = {}
    args['client_id']= CLIENT_ID

    verification_code = request.args.get("code")
    if verification_code:
        # if so, we will use code to get the access_token from Spotify
        # This corresponds to STEP 4 in https://developer.spotify.com/web-api/authorization-guide/

        args["client_secret"] = CLIENT_SECRET
        args["grant_type"] = GRANT_TYPE
        # store the code we got back from Spotify
        args["code"] = verification_code
        # the current page
        args['redirect_uri'] = request.base_url
        data = urllib.parse.urlencode(args).encode("utf-8")

        # We need to make a POST request, according to the documentation
        #headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = "https://accounts.spotify.com/api/token"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req,data=data)
        response_dict = json.loads(response.read())
        access_token = response_dict["access_token"]
        refresh_token = response_dict["refresh_token"]

        # Download the user profile. Save profile and access_token
        # in Datastore; we'll need the access_token later

        ## the user profile is at https://api.spotify.com/v1/me
        profile = json.loads(spotifyurlfetch('https://api.spotify.com/v1/me',
            access_token))

        uid = str(profile["id"])
        ## set a variable we can use to find the user later
        session['user_id'] = uid
        session['access_token'] = access_token
        ## okay, all done, send them back to the App's home page
        return redirect(url_for('index'))
    else:
        # not logged in yet-- send the user to Spotify to do that
        # This corresponds to STEP 1 in https://developer.spotify.com/web-api/authorization-guide/

        args['redirect_uri']=request.base_url
        args['response_type']="code"
        #ask for the necessary permissions -
        #see details at https://developer.spotify.com/web-api/using-scopes/
        args['scope']="user-library-modify playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private user-read-recently-played user-read-playback-state user-top-read user-library-read user-modify-playback-state app-remote-control streaming"

        url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(args)
        return redirect(url)


# Play song
@app.route("/play_song")
def play():
    if 'user_id' in session:
        sp = spotipy.Spotify(session["access_token"])
        uris = [request.args.get("uri")]
        app.logger.info("uri: " + str(uris))
        device = sp.devices()["devices"][0]["id"]
        sp.start_playback(device_id=device, uris=uris)
        return {"success":True}


# Retrieves current song
@app.route("/playing")
def retrieve_song():
    if 'user_id' in session:
        user = session["user_id"]
        sp = spotipy.Spotify(session["access_token"])
        song = sp.currently_playing()
        app.logger.info("currently playing: " + str(song))
        app.logger.info("Song name: " + str(song["item"]["name"]))
        app.logger.info("Album name: " + str(song["item"]["album"]["name"]))
        app.logger.info("Artist name: " + str(song["item"]["album"]["artists"][0]["name"]))
        current_song_info = {}
        current_song_info["song"] = song["item"]["name"]
        current_song_info["album"] = song["item"]["album"]["name"]
        current_song_info["artist"] = song["item"]["album"]["artists"][0]["name"]

        lyrics_response = retrieve_lyrics(current_song_info["artist"], current_song_info["song"])
        lyrics = lyrics_response["result"]["track"]["text"]

        current_song_info["lyrics"] = lyrics
        # app.logger.info("LYRICS: " + str())
        # potato = retrieve_lyrics("Wishes", "Beach House")
        # app.logger.info(potato)
        return json.dumps(current_song_info)


## this handler logs the user out by making the cookie expire
@app.route("/auth/logout")
def logout_handler():
    session.pop('user_id')
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)
