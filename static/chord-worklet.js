class ChordProcessor extends AudioWorkletProcessor {

    process(inputs) {

        const input = inputs[0];

        if (!input || !input[0]) {
            return true;
        }

        const samples = input[0];

        // Send the Float32 PCM buffer directly.
        // No Array.from() conversion needed.
        this.port.postMessage(samples.slice());

        return true;
    }
}

registerProcessor("chord-processor", ChordProcessor);