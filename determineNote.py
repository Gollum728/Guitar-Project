import math

def frequency_to_note(frequency):
    notes = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
    )

    semitone = round(math.log(frequency/440, 2) * 12)
    MIDI_num = 69+semitone
    note = notes[MIDI_num % 12]
    octave = str((MIDI_num//12) - 1)
    note+=octave
    print(note, frequency)

frequency_to_note(932.33)
    