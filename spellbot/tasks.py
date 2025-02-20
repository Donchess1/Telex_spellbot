import random
from celery import shared_task
from django.core.cache import cache
import requests 

def guess_words ():
    url = "https://random-word-api.herokuapp.com/word"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            word = response.json()[0]
            if len(word) == 6:
                return word

@shared_task
def start_hangman_game(channel_id):
    """Starts a new Hangman game and stores the game state in Redis."""
    hidden_word = "_" * 6
    word = guess_words()
    game_state = {
        "word": word,
        "hidden_word": hidden_word,
        "attempts_left": 6,
        "guessed_letters": []
    }
    cache.set(f"hangman_{channel_id}", game_state, timeout=600)  # Store for 10 minutes
    return {
            "event_name": "start a game",
            "message": f"🎮 **Hangman Started!** Word: {hidden_word} (Attempts left: 6)",
            "status": "success",
            "username": "Scrambot"
        }

@shared_task
def guess_hangman_letter(channel_id, user, letter):
    """Processes a player's letter guess and updates the game state."""
    game_state = cache.get(f"hangman_{channel_id}")

    if not game_state:
        return {
            "event_name": "make a guess",
            "message": "❌ No active game! Type `!hangman` to start a new one.",
            "status": "failed",
            "username": "Scrambot"
        }

    if letter in game_state["guessed_letters"]:
        return {
            "event_name": "make a guess",
            "message": f"⚠️ {user}, you already guessed '{letter}'! Try another letter.",
            "status": "failed",
            "username": "Scrambot"
        }

    game_state["guessed_letters"].append(letter)

    if letter in game_state["word"]:
        # Reveal correct letters
        new_hidden_word = "".join(
            letter if letter in game_state["guessed_letters"] else "_"
            for letter in game_state["word"]
        )
        game_state["hidden_word"] = new_hidden_word

        if "_" not in new_hidden_word:
            cache.delete(f"hangman_{channel_id}")
            return {
                "event_name": "game won",
                "message": f"🎉 {user} guessed the word **{game_state['word']}**! You win! 🎊",
                "status": "success",
                "username": "Scrambot"
            }
    else:
        game_state["attempts_left"] -= 1
        if game_state["attempts_left"] == 0:
            cache.delete(f"hangman_{channel_id}")
            return {
                "event_name": "game over",
                "message": f"💀 Game over! The correct word was **{game_state['word']}**.",
                "status": "failed",
                "username": "Scrambot"
            }

    cache.set(f"hangman_{channel_id}", game_state, timeout=600)
    
    return {
        "event_name": "make a guess",
        "message": f"{user} guessed '{letter}'. Word: {game_state['hidden_word']} (Attempts left: {game_state['attempts_left']})",
        "status": "success",
        "username": "Scrambot"
    }
