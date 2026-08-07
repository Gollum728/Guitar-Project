import librosa
import numpy as np

def pitchDetection(recording, fs):
    lowest = librosa.note_to_hz("C2")
    highest = librosa.note_to_hz("E6")
    f0, voiced_flag, voiced_prob = librosa.pyin(recording, fmin=lowest, fmax=highest, sr=fs)

    valid = (~np.isnan(f0)) & voiced_flag & (voiced_prob > 0.8)

    if np.sum(valid) == 0:
        return None

    return np.median(f0[valid])