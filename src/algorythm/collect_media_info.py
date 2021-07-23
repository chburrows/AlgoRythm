import asyncio
from time import time 
from PIL import Image
import requests
import tempfile
import numpy
from io import BytesIO
import binascii
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import spotipy_implementation as sp

async def winrtapi():
    global MediaManager, info

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

async def winrtapi_cover(info):
        # Cover Art
    import winrt
    from winrt.windows.storage.streams import \
        DataReader, Buffer, InputStreamOptions

    async def read_stream_into_buffer(stream_ref, buffer):
        readable_stream = await stream_ref.open_read_async()
        readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)
    
    # create the current_media_info dict with the earlier code first
    thumb_stream_ref = info['thumbnail']

    # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
    thumb_read_buffer = Buffer(5000000)

    # copies data from data stream reference into buffer created above
    await read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer)

    # reads data (as bytes) from buffer
    buffer_reader = DataReader.from_buffer(thumb_read_buffer)
    return buffer_reader.read_bytes(thumb_read_buffer.length) # byte buffer

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
    ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = numpy.histogram(vecs, len(codes))    # count occurrences

    max_indeces = numpy.argpartition(counts, -1 * num_colors)[-1 * num_colors:]
    colors = ["#" + binascii.hexlify(bytearray(int(c) for c in codes[i])).decode('ascii') for i in max_indeces]
    return colors

def generate_colors():
    curr_media_info = collect_title_artist()
    track_id = sp.search_for_id(*curr_media_info)
    track_img_url = sp.get_album_art(track_id)
    pil_img = get_background_img(track_img_url)
    features = sp.get_audio_features(track_id)
    tempo = float(features['track']['tempo'])
    time_per_beat = 60.0 / tempo # in sec
    time_sig = features['track']['time_signature']
    colors = generate_colors_from_img(pil_img, time_sig)
    return {'time_per_beat':time_per_beat*time_sig, 'colors':colors, 'album_art':pil_img}
if __name__ == '__main__':
    print(generate_colors())
