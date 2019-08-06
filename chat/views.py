from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.views import View
from chat.forms import loginforms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib import messages
from chat.models import USERIMAGE
from chat import urls
import json
User = get_user_model()
def index(request):
    return render(request, 'chat/index.html', {})

def room2(request, id1):
    users=Session.objects.all()
    result=[]
    roomname=''
    p=[]
    anotheruser=None
    if('_' in id1):
        k=id1.split('_')
        if(k[0]==request.user.username):
            anotheruser=k[1]
        else:
            anotheruser=k[0]
    for ses in users:
        try:
            usrid=ses.get_decoded()['_auth_user_id']
            username=User.objects.get(id=usrid).username
        except:
            usrid=None
            username=None
        try:
            u=USERIMAGE.objects.values('usr_Img').filter(user__username=username).order_by('-id')[0]
        except:
            u=None

        if(username!=None and username!=request.user.username and username not in p):
            p.append(username)
            l=[]
            l.append(request.user.username)
            l.append(username)
            l.sort()
            if(u==None):
                d = {
                    "user": username,
                    "image": "images/default-user.png",
                    "roomname": str(l[0] + "_" + l[1])
                }
            else:
                d = {
                    "user": username,
                    "image": u['usr_Img'],
                    "roomname": str(l[0] + "_" + l[1])
                }
            result.append(d)
    try:
        anotherImage = USERIMAGE.objects.values('usr_Img').filter(user__username=anotheruser).order_by('-id')[0]
    except:
        anotherImage = None
    if anotherImage == None:
        anotheContent={
        'user':anotheruser,
        "image":"images/default-user.png",

        }
    else:
        anotheContent = {
            'user': anotheruser,
            "image": anotherImage['usr_Img'],

        }
    try:
        image=USERIMAGE.objects.all().filter(user=User.objects.get(username=request.user.username)).order_by('-id')[0]
    except IndexError:
        image=None
    return render(request, 'chat/room2.html', {
        'room_name_json': mark_safe(json.dumps(id1)),
        'username': mark_safe(json.dumps(request.user.username)),
        'usernameDIS': request.user.username,
        'image':image,
        'users':result,
        'otherUser':anotheContent,

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
class profileView(View):
    def get(self,request,*arg,**kwargs):
        userform=loginforms.imageFORM()
        return render(
            request,
            template_name='chat/profile.html',
            context={
                'profile':userform,
                'username':request.user.username
            }
        )
    def post(self,request,*arg,**kwargs):
        form=loginforms.imageFORM(request.POST,request.FILES)
        if(form.is_valid()):
            form=form.save(commit=False)
            form.user=User.objects.get(username=request.user.username)
            form.save()
            return redirect('chat')
        else:
            return redirect('profile',kwargs["id1"])