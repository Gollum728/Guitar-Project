class ChordProcessor extends AudioWorkletProcessor {

    process(inputs) {

        const input = inputs[0];

        if (!input || !input[0]) {
            return true;
        }

        const samples = input[0];

        // Copy the Float32 samples so the buffer
        // remains valid after process() returns.
        const recording = new Float32Array(samples);

        this.port.postMessage(Array.from(recording));

        return true;
    }
}

registerProcessor("chord-processor", ChordProcessor);