import math

notes = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
    )
def frequency_to_note(detectedFrequency):
    semitone = round(math.log(detectedFrequency/440, 2) * 12)
    MIDI_num = 69+semitone
    note = notes[MIDI_num % 12]
    octave = str((MIDI_num//12) - 1)
    note+=octave


    targetFrequency = 440 * (2**(semitone/12))

    return (note, MIDI_num, targetFrequency)


def determineCents(detectedFrequency, expectedFrequency):
    cents = 1200 * math.log((detectedFrequency/expectedFrequency), 2)
    return cents
