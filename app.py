from flask import Flask, render_template, jsonify
from tuner import tune

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


if __name__ == "__main__":
    app.run(debug=True)