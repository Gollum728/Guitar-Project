import numpy as np

def _highestPeak(frequency, magnitude):
    max = np.argmax(magnitude)
    return frequency[max]
