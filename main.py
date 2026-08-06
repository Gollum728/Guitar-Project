import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import determineNote
import plot
import record
from Pitch_Detection import detector

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

def tune():
    IN_TUNE_THRESHOLD = 5
    recording, soundFS = record.recordAndReturn(2)
    recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended


    mask = np.abs(recording) > 0.02

    if not np.any(mask):
        print("No note detected - try again.")
        exit()    # or continue if this is inside a loop

    start = max(0, np.argmax(mask) - int(0.02 * fs))


    recording = recording[start:start + int(1.0 * fs)]
    print(np.max(np.abs(recording)))

    

    pitch = detector.pitchDetection(recording, soundFS)
    note, midi, targetFrequency = determineNote.frequency_to_note(pitch)
    cents = determineNote.determineCents(pitch, targetFrequency)
    output = f"Note : {note} \n Played frequency : {pitch} \n Expected frequency : {targetFrequency} \n Cents : {cents} \n"
    if abs(cents) <= IN_TUNE_THRESHOLD:
        output += f"In tune"
    elif cents > 0:
        output += f"Tune down"
    else:
        output += f"Tune up"
    print(output)

tune()

#while True:






