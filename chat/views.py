from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, id1):

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(id1))
    })
def login(request):
    return render(request,'chat/login.html',{})
