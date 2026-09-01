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
            audio: {
                echoCancellation: false,
                noiseSuppression: false,
                autoGainControl: false
            }
        });


        /*
            Request the same sample rate used by the
            old Python sounddevice recorder.
        */
        audioContext = new AudioContext({
            sampleRate: 44100
        });

        console.log(
            "Sample rate:",
            audioContext.sampleRate
        );


        // Load chord processor
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

        let totalSamples = 0;

        const TARGET_SAMPLES =
            Math.floor(
                0.75 * audioContext.sampleRate
            );


        processor.port.onmessage = (event) => {

            const samples = event.data;

            chunks.push(samples);

            totalSamples += samples.length;

        };


        // Microphone → processor
        audioSource.connect(processor);


        /*
            Wait until we have collected exactly
            0.75 seconds worth of audio.

            This is preferable to using setTimeout()
            because the browser's audio processing
            does not necessarily line up perfectly
            with the requested time.
        */
        await new Promise(resolve => {

            const checkSamples = () => {

                if (totalSamples >= TARGET_SAMPLES) {

                    resolve();

                } else {

                    requestAnimationFrame(checkSamples);

                }

            };

            checkSamples();

        });


        // Stop audio processing
        audioSource.disconnect();
        processor.disconnect();


        stream.getTracks().forEach(
            track => track.stop()
        );


        /*
            Combine all Float32 chunks into one recording.
        */

        const recording =
            new Float32Array(totalSamples);

        let offset = 0;


        for (const chunk of chunks) {

            const remaining =
                TARGET_SAMPLES - offset;

            const length =
                Math.min(
                    chunk.length,
                    remaining
                );

            recording.set(
                chunk.subarray(0, length),
                offset
            );

            offset += length;

            if (offset >= TARGET_SAMPLES) {
                break;
            }

        }


        console.log(
            "Recording samples:",
            recording.length
        );

        console.log(
            "Recording seconds:",
            recording.length /
            audioContext.sampleRate
        );


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
            document.getElementById(
                "confidence-status"
            );


        statusEl.textContent =
            isConfident
                ? "CONFIDENT"
                : "UNCERTAIN";


        statusEl.className =
            "status " +
            (
                isConfident
                    ? "confident"
                    : "uncertain"
            );


        const secondGuessEl =
            document.getElementById(
                "second-guess"
            );


        if (!isConfident) {

            secondGuessEl.textContent =
                `Could also be ${data.secondBest}`;

            secondGuessEl.classList.add(
                "visible"
            );

        } else {

            secondGuessEl.classList.remove(
                "visible"
            );

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