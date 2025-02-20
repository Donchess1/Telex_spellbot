from django.urls import path
from .views import HangmanGameView, get_markdown_json

urlpatterns = [
    path('hangman/', HangmanGameView.as_view(), name='hangman-api'),
    path('markdown/', get_markdown_json),
]