from django.contrib import admin
from .models import HangmanScore

@admin.register(HangmanScore)
class HangmanScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'games_played', 'games_won', 'last_played')
    list_filter = ('last_played',)
    search_fields = ('user__username',)
    readonly_fields = ('last_played',)
