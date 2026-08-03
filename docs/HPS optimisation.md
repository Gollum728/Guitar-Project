Hann Windowing
Multiplies the audio by a smooth function before the FFT. FFT assumes that the signal repeats forever because at its core, the signal is made up of sine and cosine waves, which repeat forever. If there is an abrupt sound at the end but not at the start, when we repeat the wave it creates inconsistencies, which could mean the wrong frequency is detected. The aim for this is to reduce spectral leakage, which is energy from one frequency spreading to adjacent FFT bins because the sampled waveform doesn't complete an exact number of cycles.
One important thing to note is that while this does help, if there are harmonics present, then it can still interfere with the fundamental. The Hann Window just helps for a more accurate FFT, but if the FFT itself is flawed, then no amount of windowing will help distinguish a harmonic from a fundamental.

Parabolic Interpolation
Frequencies are in bins, so when a magnitude is highest it returns that specific bin that the signal came from. Problem is, bins go up in intervals, and they can't cover each frequency. So HPS may return a frequency, but it may not be 100% accurate due to the spacing between bins. This is where parabolic interpolation comes in.
So HPS finds the index of the strongest magnitude and uses that for the frequency. Let's call that index k. We then find values at indices k-1 and k+1. We have 3 points now. We assume the spectrum near the peak can be approximated by a quadratic passing through these three points, and then find the turning point of that graph, which will give us the offset - how far away it is from the point HPS found. 
Note - you may think the points are something like (k, magnitude[k]) and similar for k-1 and k+1. To make it simpler, we say the x coordinates are -1,0,1 for k-1, k and k+1 - since it doesn't really matter. The main thing we need are the y-coordinates of each, which don't change in any way.
This entire problem is a simple A-Level Maths question - "You are given 3 points. Find the turning point of the quadratic graph that goes through these 3 points" with a couple extra steps. The full mathematical proof is shown below:
Quadratic:

y = ax² + bx + c

Three points:

(-1, α)
(0, β)
(1, γ)

Substitute into quadratic:

α = a - b + c
β = c
γ = a + b + c

Therefore:

c = β

a = (α + γ - 2β) / 2

b = (γ - α) / 2

Differentiate:

dy/dx = 2ax + b

Turning point:

2ax + b = 0

x = -b / 2a

Substitute a and b:

Offset = (α - γ) / (2(α - 2β + γ))

where

α = magnitude[k-1]
β = magnitude[k]
γ = magnitude[k+1]

Bin size:

BinSize = frequency[k] - frequency[k-1]

Interpolated frequency:

NewFrequency = frequency[k] + Offset × BinSize 