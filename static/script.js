let stream = null;
let socket = null;
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

const HOLD_TIME = 400;
const NOTE_CONFIRMATIONS = 3;


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
            audio: true
        });

        // Connect to Flask
        socket = new WebSocket(
            (window.location.protocol === "https:" ? "wss://" : "ws://")
            + window.location.host
            + "/audio"
        );

        // --------------------------------------------------
        // Receive tuner results from Python
        // --------------------------------------------------

        socket.onmessage = (event) => {

        const result = JSON.parse(event.data);

        if (result.type !== "tuner") {
            return;
        }

        // --------------------------------------------------
        // No pitch detected
        // --------------------------------------------------

        if (!result.note || result.frequency == null) {

            // Keep the last good result on screen briefly
            if (
                lastGoodResult !== null &&
                Date.now() - lastGoodTime < HOLD_TIME
            ) {
                updateDisplay(lastGoodResult);
            }

            return;
        }

        // We have a valid detection
        lastGoodResult = result;
        lastGoodTime = Date.now();

        // --------------------------------------------------
        // First valid detection
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
            // Smooth frequency changes
            const smoothing = 0.15;

            currentFrequency =
                currentFrequency +
                (result.frequency - currentFrequency) * smoothing;

            updateDisplay({
                ...result,
                frequency: currentFrequency
            });

            // Cancel any pending note
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

        // Only change displayed note after
        // several consistent detections
        if (pendingCount >= NOTE_CONFIRMATIONS) {

            currentNote = result.note;
            currentFrequency = result.frequency;

            pendingNote = null;
            pendingCount = 0;

            updateDisplay(result);
        }

    };
        // --------------------------------------------------
        // WebSocket opened
        // --------------------------------------------------

        socket.onopen = async () => {
            console.log("WebSocket connected");

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

            // Create PCM processor
            processor = new AudioWorkletNode(
                audioContext,
                "pcm-processor"
            );
            // --------------------------------------------------
            // Receive PCM data from AudioWorklet
            // --------------------------------------------------
            processor.port.onmessage = (event) => {

                if (
                    !socket ||
                    socket.readyState !== WebSocket.OPEN
                ) {
                    return;
                }


                socket.send(event.data);

            };

            // Microphone → processor
            audioSource.connect(processor);

            // Keep processor running
            processor.connect(
                audioContext.destination
            );

            tuning = true;
            tuneButton.textContent = "Stop Tuning";
            resetDisplay();
            statusElement.textContent = "LISTENING";
            console.log("Tuning started");

        };
        // --------------------------------------------------
        // WebSocket closed
        // --------------------------------------------------

        socket.onclose = () => {

            console.log("WebSocket disconnected");

        };
        // --------------------------------------------------
        // WebSocket error
        // --------------------------------------------------
        socket.onerror = (error) => {

            console.error(
                "WebSocket error:",
                error
            );

        };

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

    // Close WebSocket
    if (
        socket &&
        socket.readyState === WebSocket.OPEN
    ) {
        socket.close();
    }

    socket = null;

    // Reset detection state
    currentNote = null;
    currentFrequency = null;

    pendingNote = null;
    pendingCount = 0;

    lastGoodResult = null;
    lastGoodTime = 0;


    // Reset UI
    resetDisplay();


    tuneButton.textContent = "Start Tuning";

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