document.addEventListener("DOMContentLoaded", () => {
  const csrftoken = document.querySelector('[name=csrf-token]').content;
  const sendBtn = document.getElementById("sendGuess");
  const guessInput = document.getElementById("guessInput");
  const gameMessage = document.getElementById("gameMessage");
  const wordDisplay = document.getElementById("wordDisplay");
  const attemptsLeft = document.getElementById("attemptsLeft");
  const result = document.getElementById("result");

  // 🔹 Start a new game immediately when page loads
  startGame();

  async function startGame() {
    gameMessage.textContent = "🎮 Starting new game...";
    try {
      const response = await fetch("/api/hangman/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ message: "auto_start" }),
      });

      const data = await response.json();
      updateUI(data);
    } catch (err) {
      gameMessage.textContent = "⚠️ Error connecting to server.";
    }
  }

  async function sendGuess() {
    const message = guessInput.value.trim();
    if (!message) {
      gameMessage.textContent = "⚠️ Please enter a letter.";
      return;
    }

    guessInput.value = "";

    try {
      const response = await fetch("/api/hangman/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      updateUI(data);
    } catch (err) {
      gameMessage.textContent = "⚠️ Error connecting to server.";
    }
  }

  function updateUI(data) {
    if (data.new_hidden_word)
      wordDisplay.textContent = data.new_hidden_word.split("").join(" ");
    if (data.attempts_left !== undefined)
      attemptsLeft.textContent = `Chances left: ${data.attempts_left}`;
    if (data.message)
      gameMessage.textContent = data.message;

    if (data.game_over) {
      result.innerHTML = `<button id="restartBtn">We go again 🔁</button>`;
      document.getElementById("restartBtn").addEventListener("click", async () => {
        // Ensure fresh cache and state
        await fetch("/api/hangman/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ message: "!exit" }),
        });
        startGame(); // start new game immediately
      });
    } else {
      result.innerHTML = "";
    }
  }

  sendBtn.addEventListener("click", sendGuess);
  guessInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendGuess();
    }
  });
});
