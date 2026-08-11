import numpy as np


def mpm(recording, sampleRate):

    # -------------------------
    # Pre-processing
    # -------------------------

    recording = recording - np.mean(recording)

    print("Recording samples:", len(recording))
    print("Recording mean:", np.mean(recording))
    print("Recording std:", np.std(recording))
    print("Max amplitude:", np.max(np.abs(recording)))
    print("RMS:", np.sqrt(np.mean(recording ** 2)))

    # -------------------------
    # Frequency range
    # -------------------------

    maxFrequency = 1500
    minFrequency = 60

    minLag = int(sampleRate / maxFrequency)
    maxLag = min(
        int(sampleRate / minFrequency),
        len(recording) - 1
    )

    # MPM cutoff
    cutoff = 0.93

    # -------------------------
    # Calculate NSDF
    # -------------------------

    nsdf = np.zeros(maxLag + 1)

    for lag in range(1, maxLag + 1):

        numerator = np.sum(
            recording[lag:] * recording[:-lag]
        )

        denominator = (
            np.sum(recording[:-lag] ** 2)
            + np.sum(recording[lag:] ** 2)
        )

        if denominator != 0:
            nsdf[lag] = (2 * numerator) / denominator

    print(
        f"NSDF range: "
        f"{np.min(nsdf):.3f} "
        f"{np.max(nsdf):.3f}"
    )

    # -------------------------
    # Find local NSDF peaks
    # -------------------------

    peaks = []

    for lag in range(minLag + 1, maxLag - 1):

        if (
            nsdf[lag] > nsdf[lag - 1]
            and
            nsdf[lag] >= nsdf[lag + 1]
            and
            nsdf[lag] > 0
        ):
            peaks.append(lag)

    if not peaks:
        print("No peaks detected")
        return None

    # -------------------------
    # MPM peak selection
    # -------------------------

    maximumPeak = max(
        nsdf[lag]
        for lag in peaks
    )

    threshold = maximumPeak * cutoff

    print(f"Maximum peak: {maximumPeak:.3f}")
    print(f"Threshold: {threshold:.3f}")

    chosenLag = None

    # Find the FIRST peak above the threshold
    for lag in peaks:

        if nsdf[lag] >= threshold:

            chosenLag = lag
            break

    if chosenLag is None:
        print("No peak passed threshold")
        return None

    print(
        f"Chosen lag: {chosenLag}"
    )

    print(
        f"Chosen NSDF: "
        f"{nsdf[chosenLag]:.3f}"
    )

    # -------------------------
    # Parabolic interpolation
    # -------------------------

    if (
        chosenLag > 0
        and
        chosenLag < len(nsdf) - 1
    ):

        y1 = nsdf[chosenLag - 1]
        y2 = nsdf[chosenLag]
        y3 = nsdf[chosenLag + 1]

        denominator = (
            2 * (2 * y2 - y1 - y3)
        )

        if denominator != 0:

            shift = (
                (y1 - y3)
                / denominator
            )

            refinedLag = (
                chosenLag + shift
            )

        else:
            refinedLag = chosenLag

    else:
        refinedLag = chosenLag

    # -------------------------
    # Convert lag to frequency
    # -------------------------

    frequency = sampleRate / refinedLag

    print(
        f"Refined lag: "
        f"{refinedLag:.3f}"
    )

    print(
        f"Frequency: "
        f"{frequency:.2f} Hz"
    )

    return frequency