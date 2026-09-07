class PCMProcessor extends AudioWorkletProcessor {
    process(inputs) { //Rather than giving the full recording, the browser gives small chunks of audio at a time
        const input = inputs[0];
        if (!input || !input[0]) {
            return true;
        }
        const samples = input[0]; //  Gives Float32 samples from the first audio channel
        const pcm = new Int16Array(samples.length);
        for (let i = 0; i < samples.length; i++) {
            const sample = Math.max(-1, Math.min(1, samples[i]));
            pcm[i] = sample < 0
                ? sample * 0x8000
                : sample * 0x7FFF;
        }
        this.port.postMessage(pcm.buffer, [pcm.buffer]);
        return true;
    }
}

registerProcessor("pcm-processor", PCMProcessor);