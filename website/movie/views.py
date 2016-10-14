from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Genre, Movie
import ctypes
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def filter(request):
    all_genres = Genre.objects.all()
    selected_genre = None
    try:
        all_movies = Movie.objects.filter(genre_id=request.session['selected_genre_id'])
        selected_genre = Genre.objects.get(pk=request.session['selected_genre_id'])
        del request.session['selected_genre_id']
    except ObjectDoesNotExist:
        all_movies = Movie.objects.all()

    return render(request, 'filter.html', {'all_genres': all_genres, 'all_movies': all_movies, 'selected_genre': selected_genre})

def do_filter(request):
    genre_id = request.POST.get('dropdown')
    request.session['selected_genre_id'] = genre_id
    return HttpResponseRedirect(reverse('movie:filter'))

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
