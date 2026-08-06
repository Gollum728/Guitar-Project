import numpy as np

def parabolicInterpolation(k, frequency, magnitude):
    #Formula derived by me, check notes!!

    print(f"k = {k}")
    print(f"Frequency = {frequency[k]}")
    
    left = magnitude[k-1]
    centre = magnitude[k]
    right = magnitude[k+1]

    print(f"Left   : {left}")
    print(f"Centre : {centre}")
    print(f"Right  : {right}")

    denominator = left - (2 * centre) + right
    print(f"Denominator: {denominator}")

    

    binSize = frequency[k] - frequency[k-1]

    offset = (left-right) / (2*(left-(2*centre)+right))
    newFrequency = frequency[k] + (offset * binSize)
    print(f"HPS Freq. {frequency[k]}   PI Freq {newFrequency}")
    return newFrequency