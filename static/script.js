let stream;
let socket;
let audioContext;
let audioSource;
let processor;
let lastNote = null;
let noteCount = 0;
let currentNote = null;

const tuneButton = document.getElementById("tune-button");

const noteElement = document.getElementById("note");
const frequencyElement = document.getElementById("frequency");
const centsElement = document.getElementById("cents");
const statusElement = document.getElementById("status");
const targetElement = document.getElementById("target");
const indicatorElement = document.getElementById("indicator");


tuneButton.addEventListener("click", startRecording);


async function startRecording() {

    // Ask for microphone access
    stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    });


    // Connect to Flask
    socket = new WebSocket(
        "ws://" + window.location.host + "/audio"
    );


    // Receive tuner results from Python
    socket.onmessage = (event) => {

        const result = JSON.parse(event.data);

        console.log("Tuner result:", result);

        if (result.type !== "tuner") {
            return;
        }

        // Check whether this is the same note as the previous result
        if (result.note === lastNote) {
            noteCount++;
        } else {
            lastNote = result.note;
            noteCount = 1;
        }

        // Only update the tuner after seeing the same note twice
        if (noteCount >= 2) {

            currentNote = result.note;

            document.getElementById("note").textContent =
                result.note;

            document.getElementById("frequency").textContent =
                result.frequency.toFixed(2) + " Hz";

            document.getElementById("cents").textContent =
                result.cents.toFixed(1) + " cents";

            document.getElementById("target").textContent =
                "Target: " + result.targetFrequency.toFixed(2) + " Hz";

            document.getElementById("status").textContent =
                result.status.toUpperCase();
        }
    };


    socket.onopen = async () => {

        console.log("WebSocket connected");


        // Create audio context
        audioContext = new AudioContext();

        console.log(
            "Sample rate:",
            audioContext.sampleRate
        );


        // Load our PCM processor
        await audioContext.audioWorklet.addModule(
            "/static/pcm-worklet.js"
        );


        // Connect microphone to audio system
        audioSource =
            audioContext.createMediaStreamSource(stream);


        // Create PCM processor
        processor = new AudioWorkletNode(
            audioContext,
            "pcm-processor"
        );


        // Whenever PCM data is produced...
        processor.port.onmessage = (event) => {

            if (socket.readyState === WebSocket.OPEN) {

                socket.send(event.data);

            }

        };


        // Microphone → processor
        audioSource.connect(processor);


        // Start the processor
        processor.connect(audioContext.destination);


        tuneButton.textContent = "Stop Tuning";

        console.log("Tuning started");
    };
}