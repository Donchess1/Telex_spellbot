# spellbot/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from .tasks import start_hangman_game, hanger, end_hangman_game
from django.urls import reverse_lazy

def home(request):
    return render(request, "game/home.html")

class SignupView(View):
    template_name = "game/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Collect raw POST data and feed it to serializer
        data = request.POST.dict()
        serializer = SignupSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")  # or your play page
        else:
            # Re-render with errors
            return render(request, self.template_name, {"errors": serializer.errors})

class LoginView(AuthLoginView):
    template_name = "game/login.html"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("play_game")

@login_required
def play_game(request):
    return render(request, "game/play.html", {"username": request.user.username})

class HangmanGameView(APIView):
    """Handles POST requests for gameplay"""
    channel_id = "demo_channel"

    def post(self, request):
        data = request.data
        message = data.get("message", "")
        user_input = message.lower().strip()

        if not user_input:
            return Response({"message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        if user_input == "!exit":
            result = end_hangman_game(self.channel_id)
            return Response(result, status=status.HTTP_200_OK)

        elif len(user_input) == 1 and user_input.isalpha():
            result = hanger(self.channel_id, user_input)
            return Response(result, status=status.HTTP_200_OK)

        return Response(
            {"message": "Guess with a letter (a-z)."},
            status=status.HTTP_400_BAD_REQUEST,
        )
