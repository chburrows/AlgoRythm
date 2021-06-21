import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq
import time

FORMAT = pyaudio.paFloat32 # use float to restrict values between (0, 1)
CHANNELS = 1 # use 1 channel for now, can try to visualize stereo later
CHUNK = 128 # lower number is less latency, higher number improves performance
rate = 48000 # Will be set by device

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
    xf = rfftfreq(CHUNK, 1 / rate)

    #normalization of fft values - other methods could be investigated
    yl = 1.0 / (CHUNK / 2) * yf
    
    bins = list(zip(xf, yl))
    recent_frames.append(bins)
    recent_frames = recent_frames[-1 * KEEP_FRAMES:]
    
    last_freqs = xf
    last_levels = yl
    
    return (yl,pyaudio.paContinue)

def start_stream():
    global stream,p

    # Get default output device
    dev = p.get_default_output_device_info()
    def_name = dev['name']

    found_loop = False
    # Try to find a matching named device using WASAPI
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['name'][:len(def_name)] == def_name:
            # Check loopback capability
            wasapi_check = (p.get_host_api_info_by_index(dev["hostApi"])["name"]).find("WASAPI") != -1
            if wasapi_check:
                found_loop = True 
                break
    
    if not found_loop:
        # Change to prompt to change device in future
        # For now just use microphone
        print("Default output does not support loopback! Using default input.")
        dev = p.get_default_input_device_info()

    print('Using Device:',dev['name'])
    rate = int(dev['defaultSampleRate'])

    # as_loopback requires modified pyaudio from https://github.com/intxcc/pyaudio_portaudio
    # Currently only supports Python 3.7, may be able to build newer version
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = rate,
                    input = True,
                    frames_per_buffer = CHUNK,
                    as_loopback = found_loop,
                    input_device_index = dev['index'],
                    stream_callback=callback)

    stream.start_stream()

def stop_stream():
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    start_stream()
    while stream.is_active():
        if len(recent_frames) > 0:
            print(recent_frames[-1][:5])

        time.sleep(0.1)
    stop_stream()