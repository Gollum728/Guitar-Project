import sounddevice as sd
import determineNote
import record
from Pitch_Detection import detector
import time
import numpy as np
from Pitch_Detection.Algorithms import autocorrelation
from Pitch_Detection.Algorithms import mpm

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

IN_TUNE_THRESHOLD = 5
MIC_THRESHOLD = 0.005

"""
def tune():
    timer_start = time.perf_counter()

    recording, soundFS = record.recordAndReturn(0.75)
    print(f"Recording: {time.perf_counter() - timer_start:.3f}s")

    recording = recording.squeeze() # Convert shape from (samples, 1) to (samples,) so the FFT can use it as intended
    recording = recording - np.mean(recording)
    part1 = recording[:len(recording)//3]
    part2 = recording[len(recording)//3:2*len(recording)//3]
    part3 = recording[2*len(recording)//3:]

    rms = np.sqrt(np.mean(recording ** 2))
    peak = np.max(np.abs(recording))

    print(f"RMS: {rms:.5f}")
    print(f"Peak: {peak:.5f}")
        

    print(f"Analysed length: {len(recording)/fs:.3f}s")

    
    timer_start = time.perf_counter()

    #FFT
    fft = np.fft.rfft(recording * np.hanning(len(recording)))
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), 1 / soundFS)

    indices = np.argsort(magnitude)[-20:][::-1]

    for i in indices:
        print(f"{frequency[i]:.2f} Hz -> {magnitude[i]:.5f}")

    

    #Autocorrelation
    for i, part in enumerate([part1, part2, part3], 1):
        print(f"\n--- Part {i} ---")

        frequency = autocorrelation.autocorrelation(part, soundFS)

        if frequency is None:
            print("No pitch detected")
        else:
            print(f"Detected: {frequency:.2f} Hz")

    #pYIN
    pitch = detector.pitchDetection(recording, soundFS)
    print(f"Pitch detection: {time.perf_counter() - timer_start:.3f}s")
    if pitch is None:
        return None
    print(f"Detected pitch: {pitch:.2f} Hz")
    note, midi, targetFrequency = determineNote.frequency_to_note(pitch)
    cents = determineNote.determineCents(pitch, targetFrequency)

    if abs(cents) <= IN_TUNE_THRESHOLD:
        status = "In tune"
    elif cents > 0:
        status = "Tune down"
    else:
        status = "Tune up"

    print(f"Detected: {pitch:.2f} Hz | {note} | {cents:.1f} cents | {status}")
    return note, pitch, targetFrequency, cents, status
"""
fs = 44100
def tune():
    timer_start = time.perf_counter()

    recording, soundFS = record.recordAndReturn(0.75)

    recording = recording.squeeze()
    recording = recording - np.mean(recording)

    print(f"Recording: {time.perf_counter() - timer_start:.3f}s")

    rms = np.sqrt(np.mean(recording ** 2))
    peak = np.max(np.abs(recording))

    print(f"RMS: {rms:.5f}")
    print(f"Peak: {peak:.5f}")
    print(f"Analysed length: {len(recording) / soundFS:.3f}s")

    # Autocorrelation pitch detection
    pitch = autocorrelation.autocorrelation(recording, soundFS)

    if pitch is None:
        print("No pitch detected")
        return None

    print(f"Detected pitch: {pitch:.2f} Hz")

    # Convert frequency to musical note
    note, detectedFrequency, targetFrequency = determineNote.snapToKnownString(pitch)
    if note is None:
        return None

    cents = determineNote.determineCents(
        detectedFrequency,
        targetFrequency
    )

    if abs(cents) <= IN_TUNE_THRESHOLD:
        status = "In tune"
    elif cents > 0:
        status = "Tune down"
    else:
        status = "Tune up"

    print(
        f"Raw: {pitch:.2f} Hz | "
        f"Corrected: {detectedFrequency:.2f} Hz | "
        f"{note} | "
        f"{cents:.1f} cents | "
        f"{status}"
    )

    return note, detectedFrequency, targetFrequency, cents, status