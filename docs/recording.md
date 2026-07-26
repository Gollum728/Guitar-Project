Key terminology:
- Instantaneous amplitude => Exact value of the wave at any given time (the height of a wave at a specific point in time)
Using sounddevice to record:
- Set defaults for sample rate and channels
- sd.record() => Stored audio as numpy array
- The index represents the sample number
Sometimes the audio may not be as loud as desired. To counteract this issue, you can use this:
    recording = recording / np.max(np.abs(recording))
This finds the largest absolute value in the recording and divides each instantaneous amplitude by it, effectively increasing the peak amplitude to around 1, which makes the sound louder!
Notes:
*The graph isn't a different representation of the data—it is the NumPy array visualised*

Waveform plotting

plt.plot(recording)

The graph is simply a visualisation of the NumPy array.

The x-axis is sample number (or time if converted).

The y-axis is instantaneous amplitude.