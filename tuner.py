import sounddevice as sd
import determineNote
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

    recording, soundFS = record.recordAndReturn(0.75)
    print(f"Recording: {time.perf_counter() - timer_start:.3f}s")

    recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended

    

    print(f"Analysed length: {len(recording)/fs:.3f}s")

    
    timer_start = time.perf_counter()

    


    print(recording.dtype)
    pitch = detector.pitchDetection(recording, soundFS)
    print(f"Pitch detection: {time.perf_counter() - timer_start:.3f}s")
    if pitch is None:
        return None
    note, midi, targetFrequency = determineNote.frequency_to_note(pitch)
    cents = determineNote.determineCents(pitch, targetFrequency)

    if abs(cents) <= IN_TUNE_THRESHOLD:
        status = "In tune"
    elif cents > 0:
        status = "Tune down"
    else:
        status = "Tune up"

    return note, pitch, targetFrequency, cents, status