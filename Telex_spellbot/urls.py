
from django.contrib import admin
from django.urls import path, include
from spellbot.views import HangmanGameView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hangman/', HangmanGameView.as_view(), name="hangman_api"),
    path('', include('spellbot.urls')),
]
