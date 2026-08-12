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


def snapToKnownString(frequency):
    maxCent = 50
    OPEN_STRINGS = {
        "E2": 82.41,
        "A2": 110.00,
        "D3": 146.83,
        "G3": 196.00,
        "B3": 246.94,
        "E4": 329.63,
    }

    best_name, best_freq, best_diff_cents = None, None, float("inf")

    for name, target in OPEN_STRINGS.items():
        for octave_variant in (frequency, frequency / 2, frequency * 2):
            centsDiff = abs(determineCents(octave_variant, target))
            if centsDiff < best_diff_cents:
                best_diff_cents = centsDiff
                best_name = name
                best_freq = octave_variant
    
    if best_diff_cents > maxCent:
        return None, None, None
    return best_name, best_freq, OPEN_STRINGS[best_name]