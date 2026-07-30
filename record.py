import sounddevice as sd
import numpy as np
import soundfile as sf

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1


def _recordAudio(duration):
    recording = sd.rec(int(duration * fs))
    sd.wait()
    peak = np.max(np.abs(recording))
    if peak > 0:
        recording = recording/peak # Increases the amplitude of the recording so that it becomes louder
    return recording

def recordAndSave():
    audio = _recordAudio(5)
    sf.write("recordings/talking-test-demo.wav", audio, fs)
    
def recordAndReturn():
    audio = _recordAudio(3)
    return audio, fs

def readAudioFile(filename):
    recording, soundFS = sf.read("recordings/guitar-c4.wav")
    return recording, soundFS

