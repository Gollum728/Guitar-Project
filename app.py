from flask import Flask, render_template, jsonify
from tuner import tune
from Chord_Detection import chordDetector
from flask_sock import Sock
import numpy as np

app = Flask(__name__)
sock = Sock(app)

@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/tuner")
def tuner():
    return render_template("index.html")


@sock.route("/audio")
def audio_stream(ws):

    print("WebSocket connected")

    WINDOW_SIZE = 9600

    audio_buffer = np.array([], dtype=np.int16)

    while True:

        data = ws.receive()

        if data is None:
            break

        audio = np.frombuffer(data, dtype=np.int16)

        audio_buffer = np.concatenate((audio_buffer, audio))

        if len(audio_buffer) > WINDOW_SIZE:
            audio_buffer = audio_buffer[-WINDOW_SIZE:]

        print("Buffer:", len(audio_buffer), "samples")


@app.route("/tunerLogic")
def run_tuner():
    result = tune()

    if result is None:
        return jsonify({"error": "No note detected"})

    note, frequency, target_frequency, cents, status = result

    return jsonify({
        "note": note,
        "frequency": frequency,
        "target_frequency": target_frequency,
        "cents": cents,
        "status": status
    })

@app.route("/chord")
def showChordPage():
    return render_template("chordPage.html")

@app.route("/chordLogic")
def chordLogic():
    result = chordDetector.detectChord()
    if result == None:
        return jsonify({"error": "No chord detected"})
    best, confidence, secondBest, scores = result
    return jsonify({
        "best" : best,
        "confidence" : confidence,
        "secondBest" : secondBest
    })


@app.route("/audioTest")
def audioTest():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)
