import numpy

notes = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
)

def buildTriad(root, offsets):
    triad = []
    rootIndex = notes.index(root)
    for offset in offsets:
        nextNoteIndex = (rootIndex+offset) % 12
        nextNote = notes[nextNoteIndex]
        triad.append(nextNote)
    return triad

print(buildTriad("C", (0,3,7)))