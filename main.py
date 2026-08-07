import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import determineNote
import plot
import record
from Pitch_Detection import detector
import time

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

IN_TUNE_THRESHOLD = 5
MIC_THRESHOLD = 0.005

def tune():
    timer_start = time.perf_counter()
    analysis_duration = int(0.5 * fs)

    recording, soundFS = record.recordAndReturn(0.75)
    print(f"Recording: {time.perf_counter() - timer_start:.3f}s")

    recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended

    

    print(f"Analysed length: {len(recording)/fs:.3f}s")


    # mask = np.abs(recording) > MIC_THRESHOLD

    # if not np.any(mask):
    #     print("No note detected - try again.")
    #     return None
    # start_sample = max(0, np.argmax(mask) - int(0.02 * fs))
    
    # print(f"Recording length: {len(recording)/fs:.3f}")
    # print(f"Start: {start_sample/fs:.3f}")
    # print(f"Remaining: {(len(recording)-start_sample)/fs:.3f}")


    

    # recording = recording[start_sample:start_sample + analysis_duration]
    # print(np.max(np.abs(recording)))
    # print(f"Analysed length: {len(recording)/fs:.3f}s")

    
    timer_start = time.perf_counter()

    


    print(recording.dtype)
    pitch = detector.pitchDetection(recording, soundFS)
    print(f"Pitch detection: {time.perf_counter() - timer_start:.3f}s")
    if pitch is None:
        return None
    note, midi, targetFrequency = determineNote.frequency_to_note(pitch)
    cents = determineNote.determineCents(pitch, targetFrequency)



    return note, pitch, targetFrequency, cents
    
   



while True:
    result = tune()
    if result is None:
        continue
    note, pitchPlayed, targetFrequency, cents = result
    output = f"Note : {note} \n Played frequency : {pitchPlayed} \n Expected frequency : {targetFrequency} \n Cents : {cents} \n"
    if abs(cents) <= IN_TUNE_THRESHOLD:
        output += f"In tune"
    elif cents > 0:
        output += f"Tune down"
    else:
        output += f"Tune up"
    print(output)





