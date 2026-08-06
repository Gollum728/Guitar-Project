import librosa
import numpy as np

def pitchDetection(recording, fs):
    lowest = librosa.note_to_hz("C2")
    highest = librosa.note_to_hz("C7")
    f0, voiced_flag, voiced_prob = librosa.pyin(recording, fmin=lowest, fmax=highest, sr=fs)

    valid = f0[~np.isnan(f0)]

    if len(valid) == 0:
        return None

    return np.median(valid)