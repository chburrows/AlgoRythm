import asyncio
from PIL import Image
import requests
import tempfile
from io import BytesIO
import binascii
import numpy as np
from scipy import cluster
import algorythm.spotipy_implementation as sp


async def winrtapi():
    import winrt
    # Song info    
    from winrt.windows.media.control import \
        CurrentSessionChangedEventArgs, GlobalSystemMediaTransportControlsSessionManager as MediaManager

    sessions = await MediaManager.request_async()

    curr_session = sessions.get_current_session()
    if curr_session:
        return await curr_session.try_get_media_properties_async()
    else:
        return None

def collect_title_artist():
    info = asyncio.run(winrtapi())

    if info is not None:
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        info_dict['genres'] = list(info_dict['genres'])

        title_artist = [info_dict['title'], info_dict['artist']]
        return title_artist
    else:
        return ["N/A", "N/A"]

def get_background_img(img_url):
    buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        downloaded = 0
        for chunk in r.iter_content(chunk_size=1024):
            downloaded += len(chunk)
            buffer.write(chunk)
        buffer.seek(0)
        i = Image.open(BytesIO(buffer.read()))
    buffer.close()
    return i

def generate_colors_from_img(img, num_colors):
    NUM_CLUSTERS = 5

    rgb_img = img.convert('RGB')
    ar = np.asarray(rgb_img)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    codes, dist = cluster.vq.kmeans(ar, NUM_CLUSTERS)
    vecs, dist = cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences
    num_colors = len(counts) if len(counts) < num_colors else num_colors
    
    max_indeces = np.argpartition(counts, -1 * num_colors)[-1 * num_colors:]
    colors = [binascii.hexlify(bytearray(int(c) for c in codes[i])).decode('ascii') for i in max_indeces]
    return colors

def generate_colors(count=0):
    curr_media_info = collect_title_artist()
    # Check if no currently playing track was found
    if curr_media_info == ["N/A", "N/A"] or '' in curr_media_info:
        return {'time_per_beat':1, 'colors':None, 'album_art':None}

    track_id = sp.search_for_id(*curr_media_info)
    track_img_url = sp.get_album_art(track_id)
    pil_img = get_background_img(track_img_url)
    features = sp.get_audio_features(track_id)
    tempo = float(features['track']['tempo'])
    time_per_beat = 60.0 / tempo # in sec
    time_sig = features['track']['time_signature']
    count = time_sig if count == 0 else count
    colors = generate_colors_from_img(pil_img, count)
    return {'time_per_beat':time_per_beat*time_sig, 'colors':colors, 'album_art':pil_img}
  
if __name__ == '__main__':
    print(generate_colors())
