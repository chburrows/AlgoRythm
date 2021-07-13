#  function methodology for obtaining media information adapted from https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python
#  all intellectual credit given to original author
import asyncio
from time import time 
from numpy.lib.arraysetops import unique
from algorythm.settings import rgb_to_hex
from PIL import Image
import numpy

async def winrtapi():
    global MediaManager, info

    import winrt
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

#  Building the color palette and obtaining the top 10 most frequent colors in an image
#  Logic and functionality inspired by https://stackoverflow.com/questions/18801218/build-a-color-palette-from-image-url

def generate_colors():
    img = collect_album_cover()
    # convert bytes to RGB values
    rgb_img = img.convert('RGB')
    # make data contiguous for ordering purposes
    arr = numpy.ascontiguousarray(rgb_img)
    # flatten to manipulate 
    arr = arr.ravel()
    # get the unique colors of the array
    palette, unique_index = numpy.unique(arr, return_inverse=True)
    # make array 1D as opposed to ND
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    num_unique = numpy.bincount(unique_index)
    sorted = numpy.argsort(num_unique)
    palette = palette[sorted[::-1]]
    # return top 5 colors in the image as hex codes
    hex_codes = []
    for i in palette[:5]:
       hex_codes[i] = rgb_to_hex(palette[i])
    return hex_codes

if __name__ == '__main__':
    start = time()
    title, artist = curr_media_info = collect_title_artist()
    end = time() - start
    print(curr_media_info, end)
