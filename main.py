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



recording, soundFS = record.recordAndReturn()
recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended

# sd.play(recording)
# sd.wait()
print(type(recording))
print(recording.max())
print(recording.shape) # Returns the number of samples taken and the channels used to record




pitch = pitchDetection.detectFrequency(recording, soundFS, method="hps")
print(pitch)
print(determineNote.frequency_to_note(pitch))
# print(magnitude[max])
# print(frequency[max])

# indices = np.argsort(magnitude)[-50:]
# indices = indices[::-1]

# for i in indices:
#     print(f"{frequency[i]:8.2f} Hz   {magnitude[i]:8.2f}   {i}")


