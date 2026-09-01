let stream = null;
let audioContext = null;
let audioSource = null;
let processor = null;

let tuning = false;

let currentNote = null;
let currentFrequency = null;

let pendingNote = null;
let pendingCount = 0;

let lastGoodResult = null;
let lastGoodTime = 0;
let lastDetectionTime = 0;

const HOLD_TIME = 500;
const NOTE_CONFIRMATIONS = 2;


// --------------------------------------------------
// Elements
// --------------------------------------------------

const tuneButton = document.getElementById("tune-button");

const noteElement = document.getElementById("note");
const frequencyElement = document.getElementById("frequency");
const centsElement = document.getElementById("cents");
const statusElement = document.getElementById("status");
const targetElement = document.getElementById("target");
const indicatorElement = document.getElementById("indicator");


// --------------------------------------------------
// Start / Stop button
// --------------------------------------------------

tuneButton.addEventListener("click", () => {

    if (tuning) {
        stopTuning();
    } else {
        startRecording();
    }

});


// --------------------------------------------------
// Start tuning
// --------------------------------------------------

async function startRecording() {

    try {

        // Ask for microphone access
        stream = await navigator.mediaDevices.getUserMedia({
            audio: {
                echoCancellation: false,
                noiseSuppression: false,
                autoGainControl: false
            }
        });


        // Create audio context
        audioContext = new AudioContext();

        console.log(
            "Sample rate:",
            audioContext.sampleRate
        );


        // Load PCM processor
        await audioContext.audioWorklet.addModule(
            "/static/pcm-worklet.js"
        );


        // Connect microphone
        audioSource =
            audioContext.createMediaStreamSource(stream);


        // Create processor
        processor = new AudioWorkletNode(
            audioContext,
            "pcm-processor"
        );


        // --------------------------------------------------
        // Audio buffer
        // --------------------------------------------------

        let audioBuffer = [];


        // Use 0.5 seconds of audio instead of 1 second
        const WINDOW_SIZE =
            Math.floor(audioContext.sampleRate * 0.5);


        // Analyse every 0.1 seconds
        const STEP_SIZE =
            Math.floor(audioContext.sampleRate * 0.1);


        let samplesSinceAnalysis = 0;
        let processing = false;


        // --------------------------------------------------
        // Receive PCM data
        // --------------------------------------------------

        processor.port.onmessage = async (event) => {

            const pcm =
                new Int16Array(event.data);


            // Add new samples
            audioBuffer.push(...pcm);

            samplesSinceAnalysis += pcm.length;


            // Not enough new audio yet
            if (audioBuffer.length < WINDOW_SIZE) {
                return;
            }


            // Wait until another 0.1 seconds of audio
            // has arrived before analysing again
            if (samplesSinceAnalysis < STEP_SIZE) {
                return;
            }


            // Don't overlap HTTP requests
            if (processing) {
                return;
            }


            processing = true;
            samplesSinceAnalysis = 0;


            // Take most recent window
            const recording =
                audioBuffer.slice(
                    audioBuffer.length - WINDOW_SIZE
                );


            // Keep only enough audio for overlap
            audioBuffer =
                audioBuffer.slice(
                    audioBuffer.length - WINDOW_SIZE + STEP_SIZE
                );


            try {

                // --------------------------------------------------
                // Send recording to Python
                // --------------------------------------------------

                const response =
                    await fetch(
                        "/tunerLogic",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                recording: recording,
                                sampleRate:
                                    audioContext.sampleRate
                            })
                        }
                    );


                const result =
                    await response.json();


                // --------------------------------------------------
                // No pitch detected
                // --------------------------------------------------

                if (result.error) {
                    // Keep showing the last note briefly while it decays
                    if (
                        lastGoodResult !== null &&
                        Date.now() - lastDetectionTime < HOLD_TIME
                    ) {
                        updateDisplay(lastGoodResult);
                    } else {
                        // Enough time has passed without detecting a pitch:
                        // reset the tuner display
                        noteElement.textContent = "--";
                        frequencyElement.textContent = "-- Hz";
                        centsElement.textContent = "-- cents";
                        targetElement.textContent = "Target: --";
                        statusElement.textContent = "LISTENING";

                        resetIndicator();

                        currentNote = null;
                        currentFrequency = null;

                        pendingNote = null;
                        pendingCount = 0;
                    }
                    return;
                }


                // --------------------------------------------------
                // Valid detection
                // --------------------------------------------------

                lastGoodResult = result;
                lastGoodTime = Date.now();


                // --------------------------------------------------
                // First detection
                // --------------------------------------------------

                if (currentNote === null) {

                    currentNote = result.note;
                    currentFrequency = result.frequency;

                    updateDisplay(result);

                    return;
                }
                // --------------------------------------------------
                // Same note
                // --------------------------------------------------

                if (result.note === currentNote) {

                    // Smooth frequency
                    const smoothing = 0.25;

                    currentFrequency =
                        currentFrequency +
                        (
                            result.frequency -
                            currentFrequency
                        ) * smoothing;


                    updateDisplay({
                        ...result,
                        frequency:
                            currentFrequency
                    });


                    // Cancel pending note
                    pendingNote = null;
                    pendingCount = 0;

                    return;
                }


                // --------------------------------------------------
                // Different note
                // --------------------------------------------------

                if (result.note === pendingNote) {

                    pendingCount++;

                } else {

                    pendingNote = result.note;
                    pendingCount = 1;
                }


                // Change note after consistent detections
                if (
                    pendingCount >= NOTE_CONFIRMATIONS
                ) {

                    currentNote = result.note;
                    currentFrequency = result.frequency;

                    pendingNote = null;
                    pendingCount = 0;

                    updateDisplay(result);
                }


            } catch (error) {

                console.error(
                    "Tuner request error:",
                    error
                );

            } finally {

                processing = false;
            }

        };


        // --------------------------------------------------
        // Microphone → processor
        // --------------------------------------------------

        audioSource.connect(processor);


        // Keep processor running
        processor.connect(
            audioContext.destination
        );


        tuning = true;

        tuneButton.textContent =
            "Stop Tuning";

        resetDisplay();

        statusElement.textContent =
            "LISTENING";

        console.log(
            "Tuning started"
        );


    } catch (error) {

        console.error(
            "Could not start tuning:",
            error
        );

        resetDisplay();

        statusElement.textContent =
            "MICROPHONE ERROR";
    }

}


// --------------------------------------------------
// Stop tuning
// --------------------------------------------------

function stopTuning() {

    console.log("Stopping tuner");

    tuning = false;


    // Stop microphone
    if (stream) {

        stream.getTracks().forEach(
            track => track.stop()
        );

        stream = null;
    }


    // Disconnect audio nodes
    if (audioSource) {

        audioSource.disconnect();
        audioSource = null;
    }


    if (processor) {

        processor.disconnect();
        processor = null;
    }


    // Close audio context
    if (audioContext) {

        audioContext.close();
        audioContext = null;
    }


    // Reset detection state
    currentNote = null;
    currentFrequency = null;

    pendingNote = null;
    pendingCount = 0;


    lastGoodResult = result;
    lastGoodTime = Date.now();
    lastDetectionTime = Date.now();


    // Reset UI
    resetDisplay();


    tuneButton.textContent =
        "Start Tuning";

}


// --------------------------------------------------
// Reset tuner display
// --------------------------------------------------

function resetDisplay() {

    noteElement.textContent = "--";
    frequencyElement.textContent = "-- Hz";
    centsElement.textContent = "-- cents";
    targetElement.textContent = "Target: --";
    statusElement.textContent = "READY";

    lastGoodResult = null;
    lastGoodTime = 0;

    pendingNote = null;
    pendingCount = 0;

    resetIndicator();

}


// --------------------------------------------------
// Tuning indicator
// --------------------------------------------------

function updateIndicator(cents) {

    if (!indicatorElement) {
        return;
    }


    /*
        Move the indicator according to cents.

        -50 cents = fully flat
         0 cents = perfectly in tune
        +50 cents = fully sharp
    */

    const limitedCents =
        Math.max(-50, Math.min(50, cents));


    const percentage =
        ((limitedCents + 50) / 100) * 100;


    indicatorElement.style.left =
        percentage + "%";

}


// --------------------------------------------------
// Reset indicator
// --------------------------------------------------

function resetIndicator() {

    if (!indicatorElement) {
        return;
    }

    indicatorElement.style.left = "50%";

}


// --------------------------------------------------
// Update tuner display
// --------------------------------------------------

function updateDisplay(result) {

    noteElement.textContent =
        result.note;


    frequencyElement.textContent =
        result.frequency.toFixed(2) + " Hz";


    centsElement.textContent =
        result.cents.toFixed(1) + " cents";


    targetElement.textContent =
        "Target: " +
        result.targetFrequency.toFixed(2) +
        " Hz";


    statusElement.textContent =
        result.status.toUpperCase();


    updateIndicator(result.cents);

}