#  function methodology for obtaining media information adapted from https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python
#  all intellectual credit given to original author
import asyncio
from time import time 

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


if __name__ == '__main__':
    start = time()
    title, artist = curr_media_info = collect_title_artist()
    end = time() - start
    print(curr_media_info, end)
