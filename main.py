import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import determineNote
import plot
import pitchDetection
import record

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1



#while True:
recording, soundFS = record.readAudioFile("recordings/guitar-b3.wav")
recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended


start = np.argmax(np.abs(recording) > 0.02)

recording = recording[start:start + int(0.5 * fs)]

frequency, autocorellationResults = pitchDetection.autocorrelation(recording, soundFS)
plot.plot_autocorrelation(autocorellationResults)


# sd.play(recording)
# sd.wait()
# print(type(recording))
# print(recording.max())
# print(recording.shape) # Returns the number of samples taken and the channels used to record



"""
pitch = pitchDetection.detectFrequency(recording, soundFS, method="hps")
#print(pitch)
note = determineNote.frequency_to_note(pitch)
print(f"{pitch:.2f} Hz -> {note}")
"""

# print(magnitude[max])
# print(frequency[max])

# indices = np.argsort(magnitude)[-50:]
# indices = indices[::-1]

# for i in indices:
#     print(f"{frequency[i]:8.2f} Hz   {magnitude[i]:8.2f}   {i}")


