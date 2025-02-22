from rest_framework.views import APIView
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter
from rest_framework.response import Response
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view


class HangmanGameView(APIView):
    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        # settings = [
        #     {
        #         "label": "guess_input lenght",
        #         "type": "number",
        #         "description": "Set the maximum length for incoming guess",
        #         "default": 1,
        #         "required": True
        #         },
        #     {
        #         "label": "activation input lenght",
        #         "type": "number",
        #         "description": "Set the maximum length for start word",
        #         "default": 6,
        #         "required": True
        #         },
        #         {
        #         "label": "authentication",
        #         "type": "AlphaNumeric",
        #         "description": "means of authentication",
        #         "default": "",
        #         "required": True
        #         }
        #         ]
        channel_id = "019524fa-e7e9-73f9-9b96-04432d261992"
        message = data.get("message", "")
        
        if message == "!start":
            mine = start_hangman_game(channel_id)
            response = {
                "event_name": "game status",
                "message": mine,
                "status": "success",
                "username": "spellbot"}
            print(mine)
            return Response(response, status=status.HTTP_200_OK)

        elif len(message) == 1 and message.isalpha():
            """If a single letter is sent, process it as a guess."""
            guess = guess_hangman_letter(channel_id)
            response = {
                "event_name": "game status",
                "message": guess,
                "status": "success",
                "username": "spellbot"}
            return Response(response, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_markdown_json(request):
    try:
        with open("spellbot/integrationspec.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Markdown JSON file not found"}, status=404)