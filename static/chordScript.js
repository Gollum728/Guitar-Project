const button = document.getElementById("detect-button");

let stream = null;
let audioContext = null;
let audioSource = null;
let processor = null;

button.addEventListener("click", detectChord);


async function detectChord() {

    button.disabled = true;
    button.textContent = "Listening...";

    try {

        // Ask for microphone access
        stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });


        // Create audio context
        audioContext = new AudioContext();
        console.log(audioContext.sampleRate)

        // Load existing PCM processor
        await audioContext.audioWorklet.addModule(
            "/static/chord-worklet.js"
        );


        // Connect microphone
        audioSource =
            audioContext.createMediaStreamSource(stream);


        // Create processor
        processor = new AudioWorkletNode(
            audioContext,
            "chord-processor"
        );


        // Store incoming audio chunks
        const chunks = [];

        processor.port.onmessage = (event) => {

            const samples = event.data;

            chunks.push(...samples);

        };


        // Microphone → processor
        audioSource.connect(processor);


        // Keep processor running
        processor.connect(
            audioContext.destination
        );


        // Record for 1 second
        await new Promise(resolve => {
            setTimeout(resolve, 1000);
        });


        // Stop audio processing
        audioSource.disconnect();
        processor.disconnect();


        stream.getTracks().forEach(
            track => track.stop()
        );


        /*
            Convert Int16 PCM back to the
            -1 to +1 range expected by
            the chord detector.
        */

        const recording = new Float32Array(chunks);


        // Send recording to Python
        const response = await fetch(
            "/chordLogic",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                 body: JSON.stringify({
                    recording: Array.from(recording),
                    sampleRate: audioContext.sampleRate
                })
            }
        );

        const data = await response.json();

        if (data.error) {

            document.getElementById(
                "confidence-status"
            ).textContent = "--";

            document.getElementById(
                "chord"
            ).textContent = "NO CHORD DETECTED";

            document.getElementById(
                "score"
            ).textContent = "--";

            document.getElementById(
                "second-guess"
            ).textContent = "--";

            return;
        }


        // Display result
        document.getElementById(
            "chord"
        ).textContent = data.best;


        document.getElementById(
            "score"
        ).textContent =
            `Match: ${(data.confidence * 100).toFixed(1)}%`;


        const isConfident =
            data.confidence >= 0.025;


        const statusEl =
            document.getElementById("confidence-status");


        statusEl.textContent =
            isConfident
                ? "CONFIDENT"
                : "UNCERTAIN";


        statusEl.className =
            "status " +
            (isConfident
                ? "confident"
                : "uncertain");


        const secondGuessEl =
            document.getElementById("second-guess");


        if (!isConfident) {

            secondGuessEl.textContent =
                `Could also be ${data.secondBest}`;

            secondGuessEl.classList.add("visible");

        } else {

            secondGuessEl.classList.remove("visible");

        }

    } catch (error) {

        console.error(
            "Chord detection error:",
            error
        );

    } finally {

        if (audioContext) {

            await audioContext.close();

            audioContext = null;

        }

        stream = null;
        audioSource = null;
        processor = null;


        button.disabled = false;
        button.textContent = "Detect Chord";

    }

}