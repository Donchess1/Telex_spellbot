
import os
import requests
from django.core.cache import cache

def guess_words():
    url = "https://random-word-api.herokuapp.com/word"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            word = response.json()[0]
            if len(word) == 6:
                return word
def hanger(channel_id, letter=None):
    game_state = cache.get(f"hangman_{channel_id}")

    if not game_state:
        start_hangman_game(channel_id)
        if letter:
            return guess_hangman_letter(channel_id, letter)
        else:
            return cache.get(f"hangman_{channel_id}")
    else:
        return guess_hangman_letter(channel_id, letter)


def start_hangman_game(channel_id):
    """Starts a new Hangman game and stores the game state in the cache."""
    hidden_word = "_" * 6
    word = guess_words()
    game_state = {
        "word": word,
        "hidden_word": hidden_word,
        "attempts_left": 6,
        "guessed_letters": []
    }
    cache.set(f"hangman_{channel_id}", game_state, timeout=600)
    return {
        "message": "🎮 New game started!",
        "new_hidden_word": hidden_word,
        "attempts_left": 6
    }

def end_hangman_game(channel_id):
    """Ends the current Hangman game."""
    cache.delete(f"hangman_{channel_id}")
    return {
        "message": "😒 Game ended. Thanks for playing!",
        "game_over": True
    }

def guess_hangman_letter(channel_id, letter):
    """Processes a player's letter guess and updates the game state."""
    game_state = cache.get(f"hangman_{channel_id}")

    if not game_state:
        return {"message": "❌ No active game. Start a new one with !start."}

    if letter in game_state["guessed_letters"]:
        return {"message": f"⚠️ You already guessed '{letter}'! Try another letter."}

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
                "message": f"🎉 You guessed the word correctly: {game_state['word']}! You win! 🎊",
                "new_hidden_word": new_hidden_word,
                "game_over": True
            }
    else:
        game_state["attempts_left"] -= 1
        message = f"❌ Incorrect guess '{letter}'"
        if game_state["attempts_left"] == 0:
            cache.delete(f"hangman_{channel_id}")
            return {
                "message": f"💀 Game over! The correct word was {game_state['word']}.",
                "game_over": True
            }
        else:
            cache.set(f"hangman_{channel_id}", game_state, timeout=600)
            return {
                "message": message,
                "new_hidden_word": game_state["hidden_word"],
                "attempts_left": game_state["attempts_left"]
            }

    cache.set(f"hangman_{channel_id}", game_state, timeout=600)
    return {
        "message": f"You guessed '{letter}'.",
        "new_hidden_word": game_state["hidden_word"],
        "attempts_left": game_state["attempts_left"]
    }
