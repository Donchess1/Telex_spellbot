import os
import requests
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

#Channel_ID = os.getenv("Channel_ID", "")

WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/019524fa-e7e9-73f9-9b96-04432d261992"

def send_telex_message(event_name, message, username="Scrambot"):
    """Sends a message back to Telex"""
    payload = {
        "event_name": event_name,
        "message": message,
        "status": "success",
        "username": username
    }
    requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})

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
    message= f"🎮 ** Make a guess!** Word: {hidden_word} (Attempts left: 6)"
    send_telex_message("game started", message)
    return message
def end_hangman_game(channel_id):
    if not cache.get(f"hangman_{channel_id}"):
        message= "❌ No active game! Type `!Start` to start a new one."
        send_telex_message("No game", message)
        return message
    """Ends the current Hangman game."""
    game_state = cache.get(f"hangman_{channel_id}")
    if not game_state:
        message= "❌ No active game! Type `!Start` to start a new one."
        send_telex_message("No game", message)
        return message
    message = f"😒 aborting game, How about one more?"
    send_telex_message("No game", message)
    cache.delete(f"hangman_{channel_id}")
    return message
def guess_hangman_letter(channel_id, letter):
    """Processes a player's letter guess and updates the game state."""
    game_state = cache.get(f"hangman_{channel_id}")

    if not game_state:
        message= "❌ No active game! Type `!Start` to start a new one."
        send_telex_message("No game", message)
        return message
    if letter in game_state["guessed_letters"]:
        message = f"⚠️ you already guessed '{letter}'! Try another letter."
        send_telex_message("repeated guess", message)
        return message
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
            message = f"🎉 You guessed the word correctly, **{game_state['word']}**! You win! 🎊"
            send_telex_message("game won", message)
            return
            
    else:
        game_state["attempts_left"] -= 1
        if game_state["attempts_left"] == 0:
            cache.delete(f"hangman_{channel_id}")
            message = f"💀 Game over! The correct word was **{game_state['word']}**."
            send_telex_message("game over", message)
            return message

    cache.set(f"hangman_{channel_id}", game_state, timeout=600)
    
    message = f"You guessed '{letter}'. Word: {game_state['hidden_word']} (Attempts left: {game_state['attempts_left']})"
    send_telex_message("guess attempt", message)
    return message
