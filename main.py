import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1



recording, soundFS = sf.read("recordings/humming-middle-C.wav") # Reading a sound file returns 2 things - the actual numpy recording and the sample rate it was recorded with
# sd.play(recording)
# sd.wait()
print(type(recording))
print(recording.max())
print(recording.shape) # Returns the number of samples taken and the channels used to record



fft = np.fft.rfft(recording)
magnitude = np.abs(fft)
frequency = np.fft.rfftfreq(len(recording), d=1/fs)
print(frequency[:10])

max = np.argmax(magnitude)
print(magnitude[max])
print(frequency[max])

indices = np.argsort(magnitude)[-10:]
indices = indices[::-1]

