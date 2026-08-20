from Chord_Detection import pitchClassProfile
from Chord_Detection import scoreTriads
from Chord_Detection import triadBuilder
import numpy as np
import record

QUALITIES = [
    ("major", triadBuilder.MAJOR_OFFSET),
    ("minor", triadBuilder.MINOR_OFFSET)
]

notes = triadBuilder.notes

def detectChord():
    recording, sampleRate = record.recordAndReturn(0.5)
    rms = np.sqrt(np.mean(recording ** 2))
    if rms < 0.005:
        return None
    scores = []
    pitchResults = pitchClassProfile.pitchClassProfile(recording, sampleRate)
    compressedResults = {note: value ** 0.5 for note, value in pitchResults.items()} # Reduces the effect of open strings without altering which notes are present (see notes!!)
    for note in pitchResults.keys():
        for chord in QUALITIES:
            triad = triadBuilder.buildTriad(note, chord[1])
            #oldScore = scoreTriads.scoreTriads(triad, compressedResults)

            triadProfile = triadBuilder.expectedProfileForTriad(triad)
            newScore = _cosineSimilarity(triadProfile, compressedResults)
            chordName = f"{note} {chord[0]}"
            chordScore = (chordName, triad, newScore)
            scores.append(chordScore)


    scores.sort(reverse=True, key=lambda x: x[2])
    best = scores[0]
    secondBest = scores[1]
    confidence = best[2] - secondBest[2]
    return best, confidence, secondBest
    # return scoresByOld, scoresByNew


def _cosineSimilarity(profileA, profileB):
    #Uses formula from A-Level Further Maths to work out the angle between 2 vectors!!

    vectorA = np.array([profileA[note] for note in notes]) # Both .values() need to be converted to a numpy array first for dot product!
    vectorB = np.array([profileB[note] for note in notes])

    magA = (sum(num**2 for num in vectorA)) ** 0.5
    magB = (sum(num**2 for num in vectorB)) ** 0.5
    dot = np.dot(vectorA, vectorB)
    similarity = dot/(magA * magB)
    return similarity
