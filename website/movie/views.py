from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Genre, Movie
import ctypes
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    all_movies = Movie.objects.values_list('movie_name', flat=True)
    all_movies_list = list(all_movies)
    return render(request, 'index.html', {'all_movies_list': mark_safe(all_movies_list)})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def filter(request):
    all_genres = Genre.objects.all()
    all_movies = None
    selected_genre = None
    selected_sortby = None

    # select the dropdown_sortby
    if request.POST.get('dropdown_sortby'):
        request.session['selected_sortby'] = request.POST.get('dropdown_sortby')
        selected_sortby = request.session.get('selected_sortby')
        if not request.session.get('selected_genre_id'):
            all_movies = Movie.objects.order_by(request.session.get('selected_sortby'))

        else:
            all_movies = Movie.objects.filter(genre_id=request.session.get('selected_genre_id')).order_by(request.session.get('selected_sortby'))

    # select the dropdown_genre
    if request.POST.get('dropdown_genre'):
        request.session['selected_genre_id'] = request.POST.get('dropdown_genre')
        selected_sortby = request.session.get('selected_sortby')
        if not request.session.get('selected_sortby'):
            request.session['selected_sortby'] = "movie_name"

        # select the dropdown_genre except "All Movies"
        if request.POST.get('dropdown_genre') != '0':
            selected_genre = Genre.objects.get(pk=request.session.get('selected_genre_id'))
            all_movies = Movie.objects.filter(genre_id=request.session.get('selected_genre_id')).order_by(request.session.get('selected_sortby'))

        else:
            all_movies = Movie.objects.order_by(request.session.get('selected_sortby'))

    # first time
    if not request.POST.get('dropdown_genre') and not request.POST.get('dropdown_sortby'):
        all_movies = Movie.objects.all()

    return render(request, 'filter.html', {'all_genres': all_genres, 'all_movies': all_movies, 'selected_genre': selected_genre, 'selected_sortby': selected_sortby})

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
