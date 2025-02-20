from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter

class HangmanGameView(APIView):
    """Handles Hangman game interactions via API"""

    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        user = data.get("user")
        payload = {
            "channel_id": data.get("channel_id"),
            "settings":
                {
                    "label": "startprompt",
                    "type": "alphanumeric",
                    "description": "prompt to start the game.",
                    "default": "!start",
                    "required": True
                    },
            "message": data.get("message", "").strip().lower(),
            }

        if payload["message"] == "!start":
            game_response= start_hangman_game(payload["channel_id"])
            return Response(game_response, status=status.HTTP_200_OK)

        elif len(payload["message"]) == 1 and payload["message"].isalpha():
            """If a single letter is sent, process it as a guess."""
            game_response = guess_hangman_letter(payload["channel_id"], user, payload["message"])
            return Response(game_response, status=status.HTTP_200_OK)

        return Response({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)

class TaskStatusView(APIView):
    def get(self, request, task_id):
        """Returns the status of a given Celery task."""
        result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        })