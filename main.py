from tuner import tune
from Chord_Detection import pitchClassProfile
import record
import numpy as np

IN_TUNE_THRESHOLD = 5


# while True:
#     result = tune()
#     if result is None:
#         continue
#     note, pitchPlayed, targetFrequency, cents, status = result


#result = tune()

recording, soundFS = record.recordAndReturn(1)
print("Recording samples:", len(recording))
print("Recording mean:", np.mean(recording))
print("Recording std:", np.std(recording))
print("Max amplitude:", np.max(np.abs(recording)))
print("RMS:", np.sqrt(np.mean(recording**2)))
results = pitchClassProfile.pitchClassProfile(recording, soundFS)
print(results)