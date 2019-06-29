from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.views import View
from chat.forms import loginforms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
import json

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, id1):
    return render(request, 'chat/room2.html', {
        'room_name_json': mark_safe(json.dumps(id1)),
        'username':request.user.username
    })
def log_out(request):
    logout(request)
    return redirect('login')
class loginView(View):

    def get(self,request,*args,**kwargs):
        login=loginforms.loginForm()
        return render(request,'chat/login.html',{'login':login})

    def post(self,request,*args,**kwargs):
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('chat')
        else:
            messages.error(request,'Invalid credintials')
            return redirect('login')
class signupView(View):
    def get(self,request,*args,**kwargs):
        signup=loginforms.signupForm()
        return render(
            request,
            template_name='chat/signup.html',
            context={
                'sign':signup
            }
        )
    def post(self,request,*args,**kwargs):
        form=loginforms.signupForm(request.POST)
        if( form.is_valid()):
            try:
                user=User.objects.create_user(username=request.POST['username'], password=request.POST['password'],first_name=request.POST['firstname'],
                                    last_name=request.POST['lastname'])
                user.save()
            except:
                messages.error(request, 'Invalid credintials')
                return redirect('Signup')
            return redirect('login')
        else:
            messages.error(request,'Invalid credintials')
            return redirect("Signup")