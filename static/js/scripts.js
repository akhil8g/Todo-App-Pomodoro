let timer;
let seconds = 1500; // 25 minutes

function startTimer() {
    if (!timer) {
        timer = setInterval(() => {
            if (seconds > 0) {
                seconds--;
                updateTimerDisplay();
            } else {
                clearInterval(timer);
                timer = null;
                alert("Time's up!");
            }
        }, 1000);
    }
}

function pauseTimer() {
    clearInterval(timer);
    timer = null;
}

function resetTimer() {
    clearInterval(timer);
    timer = null;
    seconds = 1500;
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    document.getElementById("timer").textContent = `${minutes}:${secs.toString().padStart(2, '0')}`;
}
