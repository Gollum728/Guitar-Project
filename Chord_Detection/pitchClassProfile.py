from Pitch_Detection.Algorithms import fft
import determineNote

notes = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
)

def pitchClassProfile(recording, sampleRate):
    magnitudes, frequencies = fft.detectFrequency(recording, sampleRate)
    pitchDict = {note:0 for note in notes}
    binFrequency = frequencies[1] - frequencies[0]
    lowerBound = int(70/binFrequency) # Gets the index of where 70Hz is
    upperBound = int(1000/binFrequency) # Gets the index of where 2000Hz is
    adjustedFrequencies = frequencies[lowerBound:upperBound+1]
    adjustedMagnitudes = magnitudes[lowerBound:upperBound+1]
    
    for index, frequency in enumerate(adjustedFrequencies):
        note, midi, targetFrequency = determineNote.frequency_to_note(frequency)
        rawNote = notes[midi%12]
        magnitude = adjustedMagnitudes[index]
        pitchDict[rawNote] += magnitude
    
    # sortedDict = dict(sorted(pitchDict.items(), key = lambda x: x[1], reverse = True)[:5])
    # for key, value in sortedDict.items():
    #     print(f"{key} -> {value}")
    return pitchDict