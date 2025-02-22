from django.urls import path
from .views import HangmanGameView
from .spec import get_markdown_json

urlpatterns = [
    path('hangman/', HangmanGameView.as_view(), name='hangman-api'),
    path('markdown/', get_markdown_json),
]