let stream;
let audioContext;
let processor;


async function startTuner() {

    // Get microphone
    stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    });


    // Create audio system
    audioContext = new AudioContext();


    // Load our audio processor
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