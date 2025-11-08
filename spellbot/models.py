# game/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class HangmanScore(models.Model):
    """
    Tracks each authenticated user's hangman performance.
    One record per user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hangman_score")
    score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user.username} - {self.score}"
