import numpy

def scoreTriads(chord, pitchData):
    chordSum = sum(pitchData[note] for note in chord)
    pitchDataSum = sum(pitchData.values())
    score = chordSum/pitchDataSum # Sum of the 3 notes / sum of all 12 notes. Works out the proportion of the total sound coming from this potential chord
    return score