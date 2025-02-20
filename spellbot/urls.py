from django.urls import path
from .views import HangmanGameView, TaskStatusView

urlpatterns = [
    path('hangman/', HangmanGameView.as_view(), name='hangman-api'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name="task_status"),
]