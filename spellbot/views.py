from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework import status
from .tasks import start_hangman_game, guess_hangman_letter
from rest_framework.response import Response

class HangmanGameView(APIView):
    def post(self, request):
        """Processes Hangman game commands and letter guesses."""
        data = request.data
        
        channel_id = "019524fa-e7e9-73f9-9b96-04432d261992"

        request_payload = data.get("Request Payload")
        content_html= request_payload.get("content")
        soup = BeautifulSoup(content_html, "html.parser")
        message = soup.get_text().strip()
        settings = []
        print(message)
        
        if message == "!start":
            start = start_hangman_game(channel_id)
            if start.status_code == 200:
                response = {
                    "event_name": "game status",
                    "message": start,
                    "status": "success",
                    "username": "spellbot"}
                return Response(response, status=status.HTTP_200_OK)

        elif len(message) == 1 and message.isalpha():
            """If a single letter is sent, process it as a guess."""
            guess = guess_hangman_letter(channel_id)
            if guess.status_code == 200:
                response = {
                    "event_name": "game status",
                    "message": guess,
                    "status": "success",
                    "username": "spellbot"}
                return Response(response, status=status.HTTP_200_OK)
        return Response({"error": "Invalid input. Send '!start' to start a game or type a letter to guess."}, status=status.HTTP_400_BAD_REQUEST)
    
