from django.shortcuts import render, redirect
from chat.models import Thread, ChatMessage


def index(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    context ={
        'Threads':threads
    }
    return render(request, "chat/messages.html", context)

