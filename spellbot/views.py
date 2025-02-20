from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter

TELEX_WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/019524fa-e7e9-73f9-9b96-04432d261992"

class HangmanGameView(APIView):
    """Handles Hangman game interactions via API"""

    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        user = data.get("user")
        channel_id = data.get("channel_id")
        message = data.get("message", "").strip().lower()


        if message == "!start":
            start_hangman_game(channel_id)
        #    return Response(game_response, status=status.HTTP_200_OK)

        elif len(message) == 1 and message.isalpha():
            """If a single letter is sent, process it as a guess."""
            guess_hangman_letter(channel_id, user, message)
          #  return Response(game_response, status=status.HTTP_200_OK)

        return Response({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)
    
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_markdown_json(request):
    try:
        with open("spellbot/integrationspec.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Markdown JSON file not found"}, status=404)