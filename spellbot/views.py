from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter, end_hangman_game
from rest_framework.response import Response

class HangmanGameView(APIView):
    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        channel_id = channel_id = data.get("channel_id")
        messages = data.get("message", "")
        soup = BeautifulSoup(messages, "html.parser")
        user_input = soup.get_text().strip().lower()if messages else ""
        settings = []
        
        if user_input == "!start":
            start_hangman_game(channel_id)
            response = {
                "event_name": "game status",
                "message": user_input,
                "status": "success",
                "username": "spellbot"}
            return Response(response, status=status.HTTP_200_OK)
            
        elif len(user_input) == 1 and user_input.isalpha():
            """If a single letter is sent, process it as a guess."""
            guess_hangman_letter(channel_id, user_input)
            response = {
                "event_name": "game status",
                "message": user_input,
                "status": "success",
                "username": "spellbot"}
            return Response(response, status=status.HTTP_200_OK)
        elif user_input == "!exit":
            end_hangman_game(channel_id)
            response = {
                "event_name": "game status",
                "message": user_input,
                "status": "success",
                "username": "spellbot"}
            return Response(response, status=status.HTTP_200_OK)
        return Response({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)    
