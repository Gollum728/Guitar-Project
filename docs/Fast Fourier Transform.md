Waveform
A pure sound (single frequency) can be represented as a sine wave with certain multipliers. This is a very uncommon scenario, as instruments rarely produce pure sine waves.
When there are multiple sounds present, then all the pure sound waves mix together to make a wave, but a very uneven wave. The wave becomes much more complex and is virtually impossible to identify the individual frequencies by eye.

Fast Fourier Transform (FFT)
The FFT decomposes a waveform into its frequency components and measures the strength of each frequency. It works by integrating the signal multiplied by e^-2 pi i x time x frequency (cycles/second), where this function is integrated for different frequencies. When the frequency is the same as the frequency of the wave, then the absolute value of the integral is at it's highest, which tells us the frequency of the wave. You can do this for a wave with multiple sounds, and the peaks won't interfere with each other, since if the frequency used isn't the same as the frequency of the wave, the absolute value of the integral is quite close to 0, which means that it doesn't interfere with other waves.

np.fft.rfft
This takes in a recording, and returns one complex coeffient (resultant vector) for each analysed frequency. It returns complex numbers because the Fourier Transform uses complex exponentials, allowing sine and cosine components to be represented simultaneously. It is called rfft because it operates on real values, not imaginary. It only returns half of the input size because it is operating on only real numbers, the FFT of a real signal Hermitian symmetric (the negative-frequency half is the complex conjugate of the positive-frequency half), only the non-negative frequencies need to be returned. For an input of length N, rfft() returns N/2 + 1 values (when N is even). Once this is done, we take the absolute values of these to obtain their magnitude, which is what we plot.
Further explanation -> A microphone records a real-valued signal (each sample is a real number, not a complex number).
The full Fourier Transform computes both positive and negative frequencies. For a real-valued signal, these contain the same information because the negative-frequency coefficients are always the complex conjugates of the corresponding positive-frequency coefficients (Hermitian symmetry).
This happens because positive and negative frequencies represent the same physical oscillation, but with opposite directions of rotation in the complex plane. Since one half can always be reconstructed from the other, rfft() only returns the non-negative frequencies, reducing both computation and memory usage. Think of it like this:
- A positive frequency corresponds to rotation in one direction on the complex plane.
- A negative frequency corresponds to rotation in the opposite direction.
- A real cosine wave satisfies cos(θ)=cos(−θ), so the physical oscillation is unchanged by changing the sign of the frequency.
- The only thing that changes is the sign of the imaginary (sine) component, so the negative-frequency coefficient is the complex conjugate of the positive-frequency coefficient.

np.fft.rfftfreq
Generates the frequency values corresponding to each FFT coefficient. The frequency of this and the magnitude from np.ff.rfft and taking the absolute value have the same index.
The arrays have matching indices because each FFT coefficient corresponds to exactly one analysed frequency.

Frequency Resolution
The spacing between adjacent FFT frequency bins is:
Δf = fs / N
where:
- fs = sample rate
- N = number of samples
Longer recordings improve frequency resolution, allowing frequencies to be measured more accurately, but reduce responsiveness.
