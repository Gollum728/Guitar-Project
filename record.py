import sounddevice as sd
import numpy as np
import soundfile as sf

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1


def _recordAudio(duration):
    recording = sd.rec(
    int(duration * fs),
    samplerate=fs,
    channels=1,
    dtype="float32"
    )
    sd.wait()
    print(recording[:10])
    print(np.max(np.abs(recording)))
    peak = np.max(np.abs(recording))
    # if peak > 0:
    #     recording = recording/peak # Increases the amplitude of the recording so that it becomes louder
    return recording

def recordAndSave():
    audio = _recordAudio(3)
    print(sd.query_devices())
    sf.write("recordings/guitar-b3.wav", audio, fs)
    print(sd.default.device)
    print(sd.default.samplerate)
    print(sd.default.channels)
    print(sd.default.dtype)
    
def recordAndReturn(duration):
    audio = _recordAudio(duration)
    return audio, fs

def readAudioFile(filename):
    recording, soundFS = sf.read(filename)
    return recording, soundFS
