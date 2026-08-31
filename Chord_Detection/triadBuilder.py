MAJOR_OFFSET = (0,4,7)
MINOR_OFFSET = (0,3,7)
# MAJ7_OFFSET = (0, 4, 7, 11)
# MIN7_OFFSET = (0, 3, 7, 10)
# DOM7_OFFSET = (0, 4, 7, 10)
# SUS4_OFFSET = (0, 5, 7)


HARMONIC_WEIGHTS = {
    1: 1.0,    # fundamental, same pitch class
    2: 0.5,    # octave, same pitch class
    3: 0.33,   # fifth
    4: 0.25,   # 2nd octave, same pitch class
    5: 0.2,    # major third
}


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

def expectedProfileForNote(root):
    rootIndex = notes.index(root)
    profile = {note : 0 for note in notes}
    samePitchWeight = HARMONIC_WEIGHTS[1] + HARMONIC_WEIGHTS[2] + HARMONIC_WEIGHTS[4]
    fifthWeight = HARMONIC_WEIGHTS[3]
    majorThirdWeight = HARMONIC_WEIGHTS[5]

    fifthNote = notes[(rootIndex+7) % 12] # Fifth is 7 semitones above root
    majorThirdNote = notes[(rootIndex+4) % 12] # 3rd is 4 semitones above root
    
    profile[root] += samePitchWeight
    profile[fifthNote] += fifthWeight
    profile[majorThirdNote] += majorThirdWeight
    return profile

def expectedProfileForTriad(triad):
    triadProfile = {note:0 for note in notes}
    for note in triad:
        noteProfile = expectedProfileForNote(note)
        for note in notes:
            triadProfile[note] += noteProfile[note]
    return triadProfile
