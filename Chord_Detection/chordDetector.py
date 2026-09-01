from Chord_Detection import pitchClassProfile
from Chord_Detection import scoreTriads
from Chord_Detection import triadBuilder
import numpy as np
import record

QUALITIES = [
    ("major", triadBuilder.MAJOR_OFFSET),
    ("minor", triadBuilder.MINOR_OFFSET),
    # ("maj7", triadBuilder.MAJ7_OFFSET),
    # ("min7", triadBuilder.MIN7_OFFSET),
    # ("7", triadBuilder.DOM7_OFFSET),
    # ("sus4", triadBuilder.SUS4_OFFSET)
]

notes = triadBuilder.notes

def detectChord(recording, sampleRate):
    rms = np.sqrt(np.mean(recording ** 2))
    if rms < 0.03:
        return None
    scores = []
    pitchResults = pitchClassProfile.pitchClassProfile(recording, sampleRate)
    
    values = np.array(list(pitchResults.values()))
    top_three = np.sort(values)[-3:]
    if np.mean(top_three) < np.mean(values) * 1.3:
        return None
    
    for note, value in pitchResults.items():
        print(f"{note}: {value:.3f}")
    compressedResults = {note: value ** 0.5 for note, value in pitchResults.items()} # Reduces the effect of open strings without altering which notes are present (see notes!!)
    for note in pitchResults.keys():
        for chord in QUALITIES:
            triad = triadBuilder.buildTriad(note, chord[1])
            oldScore = scoreTriads.scoreTriads(triad, compressedResults)
            triadProfile = triadBuilder.expectedProfileForTriad(triad)
            newScore = _cosineSimilarity(triadProfile, compressedResults)
            chordName = f"{note} {chord[0]}"
            chordScore = (chordName, triad, newScore)
            scores.append(chordScore)
            print(f"Old score {chordName} -> {oldScore}")


    scores.sort(reverse=True, key=lambda x: x[2])
    best = scores[0]
    secondBest = scores[1]

    # Reject recordings that don't sufficiently match any chord.
    if best[2] < 0.65:
        return None

    confidence = float(best[2] - secondBest[2])
    print(best[0], confidence, secondBest[0])
    return best[0], confidence, secondBest[0], scores
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
