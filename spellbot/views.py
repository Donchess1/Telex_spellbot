# game/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from .tasks import start_hangman_game, guess_hangman_letter, end_hangman_game


# --- Regular Django Views (for rendering HTML) ---
def home(request):
    return render(request, "game/home.html")


def play(request):
    """Start game and render play.html"""
    channel_id = "demo_channel"
    start_hangman_game(channel_id)
    return render(request, "game/play.html")


# --- DRF API View for handling frontend requests ---
class HangmanGameView(APIView):
    """Handles POST requests from the JS frontend for gameplay"""
    channel_id = "demo_channel"

    def post(self, request):
        data = request.data
        message = data.get("message", "")

        # Clean and normalize input
        user_input = message.lower()

        if not user_input:
            return Response({"message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        elif user_input == "!exit":
            result = end_hangman_game(self.channel_id)
            return Response(result, status=status.HTTP_200_OK)

        elif len(user_input) == 1 and user_input.isalpha():
            result = guess_hangman_letter(self.channel_id, user_input)
            return Response(result, status=status.HTTP_200_OK)

        elif user_input == "!start":
            result = start_hangman_game(self.channel_id)
            return Response(result, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid command. Use '!start', '!exit', or guess a letter (a-z)."},
            status=status.HTTP_400_BAD_REQUEST,
        )
