# spellbot/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, SignupView, home, play_game, HangmanGameView

urlpatterns = [
    path("", home, name="home"),
    path("play/", play_game, name="play_game"),
    path("hangman/", HangmanGameView.as_view(), name="hangman_api"),

    # 🔐 Auth routes
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
]
