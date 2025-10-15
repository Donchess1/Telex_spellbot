from django.urls import path
from .views import HangmanGameView, play, home
from .spec import get_markdown_json


urlpatterns = [
    path('', home, name='home'),
    path('hangman/', HangmanGameView.as_view(), name='hangman-api'),
    path('markdown/', get_markdown_json),
    path("play/", play, name="play"),
]