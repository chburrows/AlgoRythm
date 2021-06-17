import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq
import time

FORMAT = pyaudio.paFloat32
CHANNELS = 1 # use 1 channel for now, can try to visualize stereo later
RATE = 48000 # Audio sample rate, shouldn't need to be adjusted
CHUNK = 1024 # lower number is less latency, higher number improves performance

KEEP_FRAMES = 100 #number of frames to keep in the list (mostly just need most recent frame)
recent_frames = []

def callback(in_data, frame_count, time_info, status):
    global recent_frames
    numpydata = np.frombuffer(in_data, dtype=np.float32)
    yf = np.abs(rfft(numpydata))
    xf = rfftfreq(CHUNK, 1 / RATE)

    yl = 1.0 / (CHUNK / 2) * yf
    bins = list(zip(xf, yl))

    recent_frames.append(bins)
    recent_frames = recent_frames[-1 * KEEP_FRAMES:]
    return (yl,pyaudio.paContinue)

def start_stream():
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if ('Stereo Mix' in dev['name'] and dev['hostApi'] == 3):
            dev_index = dev['index']
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = dev_index,
                    frames_per_buffer = CHUNK,
                    stream_callback=callback)

    stream.start_stream()


    while stream.is_active():
        #replace this with other logic for visualizer
        if len(recent_frames) > 0:
            print(recent_frames[-1][:5])

        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()

#remove this for actual use - only here for testing
start_stream()