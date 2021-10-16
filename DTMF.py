from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt


# audio config params
FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
CHANNELS = 1  # number of channels it means number of sample in every sampling
RATE = 44100  # number of sample in 1 second sampling
CHUNK = 1024  # length of every chunk
RECORD_SECONDS = 1  # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav"  # file name

# DTMF default frequence map
DTMF = {
    (1209, 697): '1',
    (1336, 697): '2',
    (1477, 697): '3',
    (1209, 770): '4',
    (1336, 770): '5',
    (1477, 770): '6',
    (1209, 852): '7',
    (1336, 852): '8',
    (1477, 852): '9',
    (1336, 941): '0',
    (1209, 941): '*',
    (1477, 941): '#',
    (1633, 697): 'A',
    (1633, 770): 'B',
    (1633, 852): 'C',
    (1633, 941): 'D',
}

low = [941, 852, 770, 697]
high = [1209, 1336, 1477, 1633]

audio = pyaudio.PyAudio()

print("recording...")
while True:
    # start Recording
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    # find fourier transform of data
    fftList = fft(data)

    lowMaxFreq = 0
    highMaxFreq = 0
    avg = 1200*np.average([np.absolute(i) for i in data])

    tmp1 = -float("Inf")
    for i in low:
        if np.absolute(fftList[i]) > avg:
            if np.absolute(fftList[i]) > tmp1:
                lowMaxFreq = i
                tmp1 = np.absolute(fftList[i])

    tmp2 = -float("Inf")
    for i in high:
        if np.absolute(fftList[i]) > avg:
            if np.absolute(fftList[i]) > tmp2:
                highMaxFreq = i
                tmp2 = np.absolute(fftList[i])

    if tmp1 != -float("Inf") and tmp2 != -float("Inf"):
        print(DTMF[(highMaxFreq, lowMaxFreq)])
    else:
        print("cant find")


audio.terminate()
