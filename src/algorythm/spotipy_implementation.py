import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

#  establish app credentials
cid = '***REMOVED***'
secret = '***REMOVED***'

#  set up Spotify API communication
auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=auth_manager)

# search for song based on artist and track name
track_name = 'PIN PIN'

def search_for_id(track_name, artist):
    search = sp.search(q="track:{} artist:{}".format(track_name, artist), limit=1, offset=0, type='track')
    track_id = search['tracks']['items'][0]['id']
    return track_id
def get_album_art(track_id):
    track = sp.track(track_id)
    images = track['album']['images']
    return images[-1]['url']
#  get audio features
def get_audio_features(track_id):
    features = sp.audio_analysis(track_id)
    return features