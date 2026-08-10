let tuning = false;

const button = document.getElementById("tune-button");


async function tune() {

    const response = await fetch("/tune");
    const data = await response.json();

    if (data.error) {
        const status = document.getElementById("status");

        status.textContent = "NO NOTE DETECTED";
        status.className = "status no-note";
        document.getElementById("status").textContent = "NO NOTE DETECTED";
        document.getElementById("note").textContent = "--";
        document.getElementById("frequency").textContent = "--";
        document.getElementById("cents").textContent = "--";


        return;
    }

    document.getElementById("note").textContent = data.note;

    document.getElementById("frequency").textContent =
        data.frequency.toFixed(2) + " Hz";

    document.getElementById("target").textContent =
        "Target: " + data.target_frequency.toFixed(2) + " Hz";

    document.getElementById("cents").textContent =
        data.cents.toFixed(1) + " cents";


    const status = document.getElementById("status");

    status.textContent = data.status.toUpperCase();

    status.className = "status";

    if (data.status === "In tune") {
        status.classList.add("in-tune");
    } else if (data.status === "Tune up") {
        status.classList.add("tune-up");
    } else if (data.status === "Tune down") {
        status.classList.add("tune-down");
    }


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