from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from django.core.cache import cache

class HangmanAPITest(TestCase):
    """Tests for the Hangman API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.channel_id = "test_channel"
        self.user = "test_user"

    @patch("spellbot.tasks.start_hangman_game.delay")
    def test_start_game(self, mock_task):
        """Test starting a new game"""
        mock_task.return_value.id = "1234"

        response = self.client.post("api/hangman/", {"channel_id": self.channel_id, "message": "!start"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Game loading!", response.json())
        self.assertEqual(response.json()["task_id"], "1234")

    @patch("spellbot.tasks.guess_hangman_letter.delay")
    def test_make_guess(self, mock_task):
        """Test making a letter guess"""
        mock_task.return_value.id = "5678"

        # Start a game first (Simulate a cached game)
        cache.set(f"hangman_{self.channel_id}", {
            "word": "django",
            "hidden_word": "______",
            "attempts_left": 6,
            "guessed_letters": []
        }, timeout=600)

        response = self.client.post("/api/hangman/", {"channel_id": self.channel_id, "user": self.user, "message": "d"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Your guess is being processed!", response.json())
        self.assertEqual(response.json()["task_id"], "5678")

    def test_invalid_input(self):
        """Test sending an invalid input"""
        response = self.client.post("/api/hangman/", {"channel_id": self.channel_id, "message": "123"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input", response.json()["error"])