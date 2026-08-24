let mediaRecorder;
let audioStream;

async function startRecording() {
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(audioStream);

    mediaRecorder.ondataavailable = (event) => {
        console.log("Received audio chunk:", event.data.size, "bytes");

        // We'll send this to Flask next
    };

    mediaRecorder.start(100);

    console.log("Recording started");
}

function stopRecording() {
    mediaRecorder.stop();

    audioStream.getTracks().forEach(track => track.stop());

    console.log("Recording stopped");
}