from django.urls import path
from .views import chat_with_gpt4

urlpatterns = [
    path('chat/', chat_with_gpt4, name='chat_with_gpt4'),
]
