# Guitar Tuner & Chord Detector

A real-time guitar tuner and chord-recognition system built in Python, using signal-processing techniques implemented from first principles.

🔗 **Live demo:** https://gollum21.pythonanywhere.com/

## Features
- Real-time pitch detection for tuning individual guitar strings
- Chord recognition (major/minor, with confidence scoring)
- Browser-based audio capture — no local installation needed to try it

## How it works
### Tuner: 
Audio is captured and analyzed using a custom implementation of the Normalized Square Difference Function (NSDF), a form of autocorrelation used to estimate pitch. A key challenge in pitch detection is harmonic ambiguity — a string's overtones can be mistaken for the true fundamental frequency, leading to octave errors. This was solved with a windowed search strategy: rather than searching the entire frequency range for the strongest signal, the algorithm searches narrow windows centred on each string's expected frequency, preventing strong harmonics from dominating the result. Parabolic interpolation is then used to refine the detected pitch beyond the resolution of a single sample.

### Chord detection: 
Since multiple notes are present simultaneously, a different approach is needed. Audio is converted to the frequency domain via FFT, then folded into a 12-note "pitch-class profile" — accumulating spectral energy by note name, independent of octave. Because a note's natural harmonics reinforce different pitch classes (e.g. a note's 3rd harmonic reinforces the pitch a fifth above it), candidate chords are scored using cosine similarity against a theoretical profile built from real harmonic-strength ratios, rather than simple peak-picking. This proved necessary after testing revealed that raw magnitude comparisons were skewed by physically doubled notes in common open-chord voicings (e.g. a note played on 3 strings simultaneously) — addressed through targeted magnitude compression once the root cause was diagnosed.

## Technical highlights
- Custom NSDF-based autocorrelation with windowed search to resolve harmonic/octave ambiguity
- FFT-based pitch-class profiling for chord detection, using harmonic-weighted expected profiles and cosine similarity for matching
- Diagnosed and resolved issues including octave errors, harmonic dominance, and note-doubling in open-string chord voicings

## Known limitations
- Chord detection is scoped to major/minor triads (7ths, sus chords not yet supported)
- Some closely related chords (e.g. relative major/minor) can occasionally be misidentified in ambiguous recordings
- As the noise from the current string to be tuned tapers off/quietens down, it sometimes reports a different note or a lower octave of the same note because the fundamental weakens compared to the harmonic

## Tech stack
Python, NumPy, Flask, JavaScript (Web Audio API)

## Setup
1. Clone the repo: `git clone https://github.com/Gollum728/Guitar-Project.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Open `http://127.0.0.1:5000` in your browser

Note: microphone access requires a secure context — `localhost` works fine, but the app will only function correctly over HTTPS if accessed from anywhere else.
