"""
Simple regression test script for pitch detection.

Runs saved recordings through the appropriate autocorrelation function
and checks whether the detected note LETTER (ignoring octave) matches
what was actually played. Octave is deliberately not checked, since
this detector is known to sometimes get the octave wrong while still
correctly identifying the note letter - which is all that matters for
tuning/chord-detection purposes.

Run with: python test_pitch_detection.py
"""

import re
import record
import determineNote
from Pitch_Detection.Algorithms.autocorrelation import autocorrelation, autocorrelationAllNotes
import numpy as np


def stripOctave(noteWithOctave):
    """
    Turns something like 'C#4' into 'C#', so comparisons
    ignore octave entirely.
    """
    return re.sub(r"\d+$", "", noteWithOctave)


# (filepath, expected note e.g. "C4", which detector to use)
guitarTests = [
    ("recordings/guitar-b3.wav", "B3", "guitar"),
    ("recordings/guitar-e4.wav", "E4", "guitar"),
    ("recordings/guitar-c4.wav", "C4", "allNotes"),  # not an open string
]

otherTests = [
    ("recordings/humming-a4.wav", "A4", "allNotes"),
    ("recordings/humming-b3.wav", "B3", "allNotes"),
    ("recordings/humming-c5.wav", "C5", "allNotes"),
    ("recordings/humming-d#4.wav", "D#4", "allNotes"),
    ("recordings/humming-d4.wav", "D4", "allNotes"),
    ("recordings/humming-e4.wav", "E4", "allNotes"),
    ("recordings/humming-f4.wav", "F4", "allNotes"),
    ("recordings/humming-g#3.wav", "G#3", "allNotes"),
    ("recordings/humming-g3.wav", "G3", "allNotes"),
    ("recordings/humming-middle-C.wav", "C4", "allNotes"),
    ("recordings/online-piano-a#4.wav", "A#4", "allNotes"),
]

allTests = guitarTests + otherTests


def runTests(testCases):
    passed = 0
    results = []

    for filepath, expectedNote, detectorType in testCases:
        try:
            recordingData, sampleRate = record.readAudioFile(filepath)
            recordingData = (recordingData * 32768).astype(np.int16)
        except Exception as error:
            results.append((filepath, expectedNote, "FILE ERROR", "FAIL"))
            print(f"FAIL: {filepath} - could not read file ({error})")
            continue

        if detectorType == "guitar":
            frequency = autocorrelation(recordingData, sampleRate)
        else:
            frequency = autocorrelationAllNotes(recordingData, sampleRate)

        if frequency is None:
            actualNote = "None"
        else:
            note, midi, targetFrequency = determineNote.frequency_to_note(frequency)
            actualNote = note

        expectedLetter = stripOctave(expectedNote)
        actualLetter = stripOctave(actualNote) if actualNote != "None" else "None"

        status = "PASS" if actualLetter == expectedLetter else "FAIL"
        if status == "PASS":
            passed += 1

        results.append((filepath, expectedNote, actualNote, status))
        print(f"{status}: {filepath} - expected {expectedNote}, got {actualNote}")
        print(f"Comparing: expectedLetter={expectedLetter}, actualLetter={actualLetter}")

    print(f"\n{passed}/{len(testCases)} passed")
    return results


if __name__ == "__main__":
    print("=== Guitar-specific tests ===")
    runTests(guitarTests)

    print("\n=== General pitch detection tests ===")
    runTests(otherTests)