from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
import ctypes
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def doesExist(username):
    for user in User.objects.all():
        if (user.get_username() == username):
            return True
    return False

def newUser(username, password):
    user = User.objects.create_user(username, None, password)
    user.save()

def authenticate(username, password):
    for user in User.objects.all():
        if (user.get_username() == username and user.check_password(password)):
            return user
    return None

def mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

def login_api(request):
    username = request.POST['username']
    password = request.POST['password']
    auth_user = authenticate(username, password)
    if(auth_user is not None):
        mbox('Success', 'Login Completed.', 0)
        return HttpResponseRedirect(reverse('movie:index'))
    else:
        mbox('Error', 'Your username or password is incorrect.', 0)
        return HttpResponseRedirect(reverse('movie:login'))

def register_api(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm-password']

    if(password != confirm_password):
        mbox('Error', 'Your password does not match.', 0)
        return None

    if (not doesExist(username)):
        newUser(username, password)
        mbox('Success', 'Register Completed.', 0)
        return HttpResponseRedirect(reverse('movie:index'))

    else:
        mbox('Error', 'Username does exist', 0)
        return None