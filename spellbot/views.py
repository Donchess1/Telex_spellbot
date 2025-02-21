from rest_framework.views import APIView
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter

import json
from django.http import JsonResponse
from rest_framework.decorators import api_view


class HangmanGameView(APIView):
    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        channel_id = data.get("channel_id")
        settings = data.get("settings", [])
        message = data.get("message").lower()

        if message == "!start":
            response = start_hangman_game(channel_id)
            print(message)
            return JsonResponse({
                "event_name": "game status",
                "message": response,
                "status": "success",
                "username": "spellbot"})

        elif len(message) == 1 and message.isalpha():
            """If a single letter is sent, process it as a guess."""
            response = guess_hangman_letter(channel_id, message)
            return JsonResponse({
                "event_name": "game status",
                "message": response,
                "status": "success",
                "username": "spellbot"})
        return JsonResponse({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_markdown_json(request):
    try:
        with open("spellbot/integrationspec.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Markdown JSON file not found"}, status=404)