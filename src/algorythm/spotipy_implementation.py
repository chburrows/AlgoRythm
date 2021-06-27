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

def search_for_id(track_name):
    search = sp.search(q=track_name, limit=1, offset=0, type='track')
    track_id = search['album']['artists']['id']
    return track_id

#  get audio features
def get_audio_features(track_id):
    features = sp.audio_features(search_for_id(track_name=track_name))
    return features
    