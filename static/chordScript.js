const button = document.getElementById("detect-button");


async function detectChord() {
    button.disabled = true;
    button.textContent = "Listening...";
    const response = await fetch("/chordLogic");
    const data = await response.json();

    if (data.error) {
        const status = document.getElementById("confidence-status");

        // status.textContent = "NO NOTE DETECTED";
        // status.className = "status no-note";
        document.getElementById("confidence-status").textContent = "--";
        document.getElementById("chord").textContent = "NO CHORD DETECTED";
        document.getElementById("score").textContent = "--";
        document.getElementById("second-guess").textContent = "--";
        button.disabled = false;
        button.textContent = "Detect Chord";
        return;
    }

    document.getElementById("chord").textContent = data.chord;

    document.getElementById("score").textContent = `Match: ${(data.score * 100).toFixed(1)}%`;


    const isConfident = data.confidence >= 0.025
    const statusEl = document.getElementById("confidence-status");
    statusEl.textContent = isConfident ? "CONFIDENT" : "UNCERTAIN";
    statusEl.className = "status " + (isConfident ? "confident" : "uncertain");
    const secondGuessEl = document.getElementById("second-guess");
    if (!isConfident){
        secondGuessEl.textContent = `Could also be ${data.secondGuess}`
        secondGuessEl.classList.add("visible")
    }
    else{
        secondGuessEl.classList.remove("visible")
    }


    button.disabled = false;
    button.textContent = "Detect Chord";

}