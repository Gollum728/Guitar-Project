import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1


# duration = 5
# recording = sd.rec(int(duration * fs))
# sd.wait()
# recording = recording / np.max(np.abs(recording)) # Increases the amplitude of the recording so that it becomes louder
# sf.write("recordings/harmonica-chromatic-scale.wav", recording, fs)
recording, soundFS = sf.read("recordings/harmonica-chromatic-scale.wav") # Reading a sound file returns 2 things - the actual numpy recording and the sample rate it was recorded with
# sd.play(recording)
# sd.wait()
print(type(recording))
print(recording.max())
print(recording.shape) # Returns the number of samples taken and the channels used to record

plt.plot(recording[75000:76000])
plt.title("Audio graph")
plt.xlabel("Time")
plt.ylabel("Height")
plt.show()
