import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq
import time

FORMAT = pyaudio.paFloat32 # use float to restrict values between (0, 1)
CHANNELS = 1 # use 1 channel for now, can try to visualize stereo later
RATE = 48000 # Audio sample rate, shouldn't need to be adjusted
chunk = 1024 # lower number is less latency, higher number improves performance

KEEP_FRAMES = 100 #number of frames to keep in the list (mostly just need most recent frame)

recent_frames = []
last_freqs = None
last_levels = None
stream = None

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    global recent_frames, last_freqs, last_levels
    
    numpydata = np.frombuffer(in_data, dtype=np.float32)
    
    yf = np.abs(rfft(numpydata))
    xf = rfftfreq(chunk, 1 / RATE)

    #normalization of fft values - other methods could be investigated
    yl = 1.0 / (chunk / 2) * yf
    
    bins = list(zip(xf, yl))
    recent_frames.append(bins)
    recent_frames = recent_frames[-1 * KEEP_FRAMES:]
    
    last_freqs = xf[:(chunk+1)//3]
    last_levels = yl[:(chunk+1)//3]
    
    return (yl,pyaudio.paContinue)

def start_stream(settings):
    global stream,p,chunk
    chunk = settings.b_count * 3 - 1

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if ('Stereo Mix' in dev['name'] and dev['hostApi'] == 3):
            dev_index = dev['index']
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = dev_index,
                    frames_per_buffer = chunk,
                    stream_callback=callback)

    stream.start_stream()

def stop_stream():
    stream.stop_stream()
    stream.close()
    p.terminate()

def restart_stream(settings):
    # clear and remake stream to update chunk
    global recent_frames, last_freqs, last_levels
    stream.stop_stream()
    stream.close()

    recent_frames = []
    last_freqs = None
    last_levels = None

    start_stream(settings)

if __name__ == '__main__':
    start_stream()
    while stream.is_active():
        if len(recent_frames) > 0:
            print(recent_frames[-1][:5])

        time.sleep(0.1)
    stop_stream()