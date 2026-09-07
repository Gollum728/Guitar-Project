let stream;
let audioContext;
let processor;


async function startTuner() {

    stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    }); // Asks for access for the user's microphone


    // Create audio system
    audioContext = new AudioContext(); // Environment where the browser processes audio


    // Load the audio processor
    await audioContext.audioWorklet.addModule(
        "/static/pcm-worklet.js"
    );


    // Turn microphone into audio source
    const source =
        audioContext.createMediaStreamSource(stream);


    // Create our processor
    processor = new AudioWorkletNode(
        audioContext,
        "pcm-processor"
    );


    // Connect microphone → processor
    source.connect(processor);


    // Receive samples from processor
    processor.port.onmessage = function(event) {

        const samples = event.data;

        console.log(samples);

    };
}