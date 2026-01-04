import os
import requests
from django.core.cache import cache
from django.contrib.auth.models import User
import random

# Fallback word list for when API is slow/unavailable
FALLBACK_WORDS = [
    "ponder", "sponge", "coding", "server", "client", "memory", "gaming", "router",
    "module", "folder", "string", "number", "object", "method", "struct", "bridge",
    "shadow", "window", "forest", "garden", "yellow", "orange", "purple", "simple",
    "double", "circle", "square", "global", "random", "junior", "senior", "master",
    "castle", "rocket", "planet", "dragon", "wizard", "knight", "magic", "potion",
    "temple", "valley", "stream", "canyon", "desert", "jungle", "arctic", "tunnel",
    "engine", "turbos", "powers", "energy", "fusion", "atomic", "cosmic", "galaxy",
    "bubble", "marble", "powder", "lectus", "silver", "golden", "bronze", "copper"
]

def guess_words(use_api=False):
    """Get a random 6-letter word with fallback and timeout handling
    
    Args:
        use_api (bool): Whether to try external API or use local words only
    """
    # For faster gameplay, prefer local words
    if not use_api:
        return random.choice(FALLBACK_WORDS).upper()
    
    url = "https://random-word-api.herokuapp.com/word"
    
    try:
        # Try external API with short timeout - if it's slow, prefer our fast fallback
        response = requests.get(url, timeout=1.5)  # Reduced to 1.5 second timeout
        if response.status_code == 200:
            word = response.json()[0]
            if len(word) == 6:
                return word.upper()
            else:
                # If word isn't 6 letters, fall back to our list
                return random.choice(FALLBACK_WORDS).upper()
    except (requests.RequestException, requests.Timeout, Exception):
        # If API fails or is slow, use fallback immediately
        pass
    
    # Fallback to predefined words - instant response
    return random.choice(FALLBACK_WORDS).upper()

def hanger(channel_id, letter=None, user=None):
    game_state = cache.get(f"hangman_{channel_id}")

    if not game_state:
        start_hangman_game(channel_id, user)
        if letter:
            return guess_hangman_letter(channel_id, letter)
        else:
            return cache.get(f"hangman_{channel_id}")
    else:
        return guess_hangman_letter(channel_id, letter)


def start_hangman_game(channel_id, user=None):
    """Starts a new Hangman game and stores the game state in the cache."""
    hidden_word = "_" * 6
    word = guess_words(use_api=False)  # Use local words for instant response
    
    # Get or create user score
    current_score = 5  # Start at middle (5/10)
    if user and user.is_authenticated:
        from .models import HangmanScore
        score_obj, created = HangmanScore.objects.get_or_create(user=user)
        current_score = max(0, min(10, score_obj.score))  # Ensure score is between 0-10
    
    game_state = {
        "word": word,
        "hidden_word": hidden_word,
        "attempts_left": 6,
        "guessed_letters": [],
        "user_id": user.id if user and user.is_authenticated else None,
        "current_score": current_score
    }
    cache.set(f"hangman_{channel_id}", game_state, timeout=600)
    return {
        "message": "🎮 New game started!",
        "new_hidden_word": hidden_word,
        "attempts_left": 6,
        "current_score": current_score
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
    
    # Helper function to update user score ONLY on game completion
    def update_user_score_on_game_end(game_won=False):
        user_id = game_state.get("user_id")
        if user_id:
            try:
                from .models import HangmanScore
                user = User.objects.get(id=user_id)
                score_obj, created = HangmanScore.objects.get_or_create(user=user)
                
                # Update score: +1 for win, -1 for loss
                score_change = 1 if game_won else -1
                new_score = max(0, min(10, game_state.get("current_score", 5) + score_change))
                
                # Update persistent user stats
                score_obj.games_played += 1
                if game_won:
                    score_obj.games_won += 1
                score_obj.score = new_score  # Save final score
                score_obj.save()
                
                return new_score
            except:
                pass
        return game_state.get("current_score", 5)

    if letter in game_state["word"]:
        # Reveal correct letters
        new_hidden_word = "".join(
            letter if letter in game_state["guessed_letters"] else "_"
            for letter in game_state["word"]
        )
        game_state["hidden_word"] = new_hidden_word

        if "_" not in new_hidden_word:
            # Word is complete - player wins! Update score +1
            final_score = update_user_score_on_game_end(game_won=True)
            cache.delete(f"hangman_{channel_id}")
            return {
                "message": f"🎉 You guessed the word correctly: {game_state['word']}! You win! 🎊",
                "new_hidden_word": new_hidden_word,
                "game_over": True,
                "current_score": final_score
            }
        else:
            # Correct letter but word not complete yet - NO score change
            cache.set(f"hangman_{channel_id}", game_state, timeout=600)
            return {
                "message": f"✅ Great guess! '{letter}' is in the word!",
                "new_hidden_word": game_state["hidden_word"],
                "attempts_left": game_state["attempts_left"],
                "current_score": game_state["current_score"]  # Keep current score unchanged
            }
    else:
        # Incorrect letter - NO score change during gameplay
        game_state["attempts_left"] -= 1
        message = f"❌ Incorrect guess '{letter}'"
        
        if game_state["attempts_left"] == 0:
            # Game over - player lost! Update score -1
            final_score = update_user_score_on_game_end(game_won=False)
            cache.delete(f"hangman_{channel_id}")
            return {
                "message": f"💀 Game over! The correct word was {game_state['word']}.",
                "game_over": True,
                "current_score": final_score
            }
        else:
            # Still have attempts left - NO score change
            cache.set(f"hangman_{channel_id}", game_state, timeout=600)
            return {
                "message": message,
                "new_hidden_word": game_state["hidden_word"],
                "attempts_left": game_state["attempts_left"],
                "current_score": game_state["current_score"]  # Keep current score unchanged
            }