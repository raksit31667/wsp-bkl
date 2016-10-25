from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Genre, Movie
from .forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from wsgiref.util import FileWrapper

class IndexView(View):
    form_class = UserForm
    template_name = 'index.html'

    def get(self, request):
        form = self.form_class(None)
        all_genres = Genre.objects.all()
        all_movies = Movie.objects.all()
        all_movies_list = list(Movie.objects.values_list('movie_name', flat=True))
        invalid_login = request.session.get('invalid_login')
        try:
            del request.session['invalid_login']
        except KeyError:
            pass
        return render(request, self.template_name, {'form': form, 'all_genres': all_genres, 'all_movies': all_movies, 'all_movies_list': mark_safe(all_movies_list), 'invalid_login': invalid_login})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            all_movies = Movie.objects.values_list('movie_name', flat=True)
            all_movies_list = list(all_movies)
            return render(request, self.template_name, {'form': form, 'all_movies_list': mark_safe(all_movies_list)})

        all_movies = Movie.objects.values_list('movie_name', flat=True)
        all_movies_list = list(all_movies)
        return render(request, self.template_name, {'form': form, 'all_movies_list': mark_safe(all_movies_list), 'invalid_register': True})

def filter(request, genre, sortby):
    all_genres = Genre.objects.all()

    if sortby:
        if genre == 'all':
            selected_movies = Movie.objects.order_by(sortby)
            selected_genre = None

        else:
            genre_id = Genre.objects.get(genre_name__iexact=genre).id
            selected_movies = Movie.objects.filter(genre_id=genre_id).order_by(sortby)
            selected_genre = Genre.objects.get(pk=genre_id)

    else:
        if genre == 'all':
            selected_movies = Movie.objects.all()
            selected_genre = None

        else:
            genre_id = Genre.objects.get(genre_name__iexact=genre).id
            selected_movies = Movie.objects.filter(genre_id=genre_id)
            selected_genre = Genre.objects.get(pk=genre_id)


    return render(request, 'filter.html', {'all_genres': all_genres, 'selected_movies': selected_movies, 'selected_genre': selected_genre, 'selected_sortby': sortby})

def search_movie(request):
    input = request.POST['typeahead']
    if len(input) == 0 :
        result = None
    else:
        result = Movie.objects.filter(movie_name__icontains=input)
    return render(request, 'search.html', {'result':result}, {'input':input})


def does_username_exist(username):
    for user in User.objects.all():
        if (user.get_username() == username):
            return True
    return False

def does_email_exist(email):
    for user in User.objects.all():
        if (user.email == email):
            return True
    return False

def newUser(username, password, email):
    user = User.objects.create_user(username, email, password)
    user.save()

def login_api(request):
    username = request.POST['username']
    password = request.POST['password']
    auth_user = authenticate(username=username, password=password)
    request.session['invalid_login'] = None
    if(auth_user is not None):
        if auth_user.is_active:
            login(request, auth_user)
        else:
            request.session['invalid_login'] = 'Your account has been disabled.'

    else:
        request.session['invalid_login'] = 'Invalid username or password.'

    return HttpResponseRedirect(reverse('movie:index'))

def download_movie(request, movie_id):
        m = Movie.objects.get(pk=movie_id)
        file = FileWrapper(open(m.movie_file.path, 'rb'))
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = str('attachment; filename='+m.movie_file.name)
        return response
        return HttpResponseRedirect('/')

class DescriptView(View):
    form_class = UserForm
    template_name = 'descrip.html'

    def get(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        movie.movie_teaser_url = self.convertLink(movie.movie_teaser_url)
        return render(request, 'descrip.html',{'movie':movie})

    def convertLink(self, link):
        str = link
        return str.replace('watch?v=', 'embed/')
