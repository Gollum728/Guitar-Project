let mediaRecorder = [];
let audioChunks = [];

async function startTestRecording(){
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavilable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop() = () => {
        const audioBlob = new Blob(audioChunks, {type: "audio/webm"});
        const audioURL = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioURL);
        audio.play();
    };

    mediaRecorder.start();
    console.log("Recording started");
};


function stopTestRecording() {
    mediaRecorder.stop();
    console.log("Recording stopped");
};