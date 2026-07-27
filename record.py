import sounddevice as sd
import numpy as np
import soundfile as sf

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

def record():
    duration = 5
    recording = sd.rec(int(duration * fs))
    sd.wait()
    recording = recording / np.max(np.abs(recording)) # Increases the amplitude of the recording so that it becomes louder
    sf.write("recordings/humming-.wav", recording, fs)

record()

