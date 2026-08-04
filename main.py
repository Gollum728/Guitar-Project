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
recording, soundFS = record.recordAndReturn(3)
recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended


mask = np.abs(recording) > 0.02

if not np.any(mask):
    print("No note detected - try again.")
    exit()    # or continue if this is inside a loop

start = max(0, np.argmax(mask) - int(0.02 * fs))


recording = recording[start:start + int(1.0 * fs)]
print(np.max(np.abs(recording)))

pitch, autocorellationResults = pitchDetection.autocorrelation(recording, soundFS)
plot.plot_autocorrelation(autocorellationResults)


# sd.play(recording)
# sd.wait()
# print(type(recording))
# print(recording.max())
# print(recording.shape) # Returns the number of samples taken and the channels used to record




#print(pitch)
note, midi, targetFrequency = determineNote.frequency_to_note(pitch)
cents = determineNote.determineCents(pitch, targetFrequency)
print(f"{pitch:.2f} Hz -> {note}")
print(cents)


# print(magnitude[max])
# print(frequency[max])

# indices = np.argsort(magnitude)[-50:]
# indices = indices[::-1]

# for i in indices:
#     print(f"{frequency[i]:8.2f} Hz   {magnitude[i]:8.2f}   {i}")


