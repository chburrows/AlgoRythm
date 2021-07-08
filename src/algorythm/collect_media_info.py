#  function methodology for obtaining media information adapted from https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python
#  all intellectual credit given to original author
import asyncio
from time import time 
import winrt

async def winrtapi():
    global MediaManager, info

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

def collect_album_cover():
    # Collect song info attributes
    info = asyncio.run(winrtapi())
    if info is not None:
        # Convert info to dictionary
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        # Pass in dictionary and retrieve img byte buffer
        img = asyncio.run(winrtapi_cover(info_dict))
        # Write bytes to jpg file 
        # TODO: return to pygame/graphics.py instead
        with open('test_img.jpg', 'wb+') as file:
            file.write(bytearray(img))
        



if __name__ == '__main__':
    title, artist = curr_media_info = collect_title_artist()
    print(curr_media_info)
    collect_album_cover()
