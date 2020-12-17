import urllib.request, urllib.error, urllib.parse, json, requests

# baseurl = "https://orion.apiseeds.com/api/music/lyric/"

artist = "Beach House"
track = "Wishes"
baseurl = "https://orion.apiseeds.com/api/music/lyric/{artist}/{track}".format(artist=artist, track=track)

API_KEY = "bZpKzQTHsIGBpOoWAvUXD1yeShaU3LgDw4UKe5f3uOuk8KWRpIk0oHFSlT8c6NVY"
params = {}

# params["artist"] = "Beach House"
# params["track"] = "Wishes"
params["apikey"] = API_KEY

url = baseurl + "?" + urllib.parse.urlencode(params)
text = requests.get(url).json()["result"]["track"]["text"]
split_text = text.split("\n")
for line in split_text:
    print(line)

# print(split_text)


# def retrieve_lyrics(artist, track):
#     params["apikey"] = LYRICS_KEY
#     baseurl = "https://orion.apiseeds.com/api/music/lyric/{artist}/{track}".format(artist=artist, track=track)
#     url = baseurl + "?" + urllib.parse.urlencode(params)
#     url = baseurl + "?" + urllib.parse.urlencode(params)
#     lyrics_response = requests.get(url).json()
#     return lyrics_response
# print(url)
# print(urllib.request.urlopen(url))

# https://orion.apiseeds.com/api/music/lyric/Beach House/Wishes?apikey=bZpKzQTHsIGBpOoWAvUXD1yeShaU3LgDw4UKe5f3uOuk8KWRpIk0oHFSlT8c6NVY
# https://orion.apiseeds.com/api/music/lyric/?artist=Beach+House&track=Wishes&apikey=bZpKzQTHsIGBpOoWAvUXD1yeShaU3LgDw4UKe5f3uOuk8KWRpIk0oHFSlT8c6NVY
