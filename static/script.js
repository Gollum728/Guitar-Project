let tuning = false;

const button = document.getElementById("tune-button");


async function tune() {

    const response = await fetch("/tune");
    const data = await response.json();

    if (data.error) {
        document.getElementById("status").textContent = "NO NOTE DETECTED";
        return;
    }

    document.getElementById("note").textContent = data.note;

    document.getElementById("frequency").textContent =
        data.frequency.toFixed(2) + " Hz";

    document.getElementById("target").textContent =
        "Target: " + data.target_frequency.toFixed(2) + " Hz";

    document.getElementById("cents").textContent =
        data.cents.toFixed(1) + " cents";


    document.getElementById("status").textContent =
        data.status.toUpperCase();


    const indicator = document.getElementById("indicator");

    const position = Math.max(-50, Math.min(50, data.cents));

    indicator.style.left = `${50 + position}%`;
}


button.addEventListener("click", async () => {

    tuning = !tuning;

    if (tuning) {

        button.textContent = "Stop Tuning";

        while (tuning) {
            await tune();
        }

    } else {

        button.textContent = "Start Tuning";

    }

});