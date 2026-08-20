from flask import Flask, render_template, jsonify
from tuner import tune
from Chord_Detection import chordDetector

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tune")
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
    best, confidence, secondBest = result
    return jsonify({
        "best" : best,
        "confidence" : confidence,
        "secondBest" : secondBest
    })



if __name__ == "__main__":
    app.run(debug=True)