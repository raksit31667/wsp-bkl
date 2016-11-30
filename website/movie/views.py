from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Avg, Count
from .models import Genre, Movie, Rating, Serial, Transaction, UserNet, UserOwn
from .forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from wsgiref.util import FileWrapper
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from random import randint
import json

def movies(request):
    movies = list(Movie.objects.values_list('movie_name', flat=True))
    return JsonResponse({'movies':movies})

def filter(request, genre, sortby):
    all_genres = Genre.objects.all()

    if sortby:
        if genre == 'all':
            if sortby == 'rating':
                selected_movies = Movie.objects.annotate(avg_rating=Avg('rating__rating')).exclude(avg_rating__isnull=True).order_by('-avg_rating')
            else:
                selected_movies = Movie.objects.order_by(sortby)
            selected_genre = None

        else:
            genre_id = Genre.objects.get(genre_name__iexact=genre).id
            if sortby == 'rating':
                selected_movies = Movie.objects.annotate(avg_rating=Avg('rating__rating')).exclude(avg_rating__isnull=True).filter(genre_id=genre_id).order_by('-avg_rating')
            else:
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


    return TemplateResponse(request, 'filter.html', {'all_genres': all_genres, 'selected_movies': selected_movies, 'selected_genre': selected_genre, 'selected_sortby': sortby})

def search_movie(request):
    input = request.POST['typeahead']
    if len(input) == 0 :
        result = None
    else:
        result = Movie.objects.filter(movie_name__icontains=input)
    return TemplateResponse(request, 'search.html', {'result':result}, {'input':input})


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
    loginable = False
    message = "success"
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    auth_user = authenticate(username=username, password=password)
    if(auth_user is not None):
        if auth_user.is_active:
            login(request, auth_user)
            loginable = True
        else:
            message = 'Your account has been disabled.'

    else:
        message = 'Invalid username or password.'

    return JsonResponse({'loginable':loginable, 'msg': message})

def register_api(request):
    registerable = True
    message = "success"
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)

    if does_email_exist(email):
        message = "This email is already registered"
        registerable = False

    if does_username_exist(username):
        message = "This username already exist"
        registerable = False

    if registerable:
        print(username)
        print(password)
        print(email)
        newUser(username, password, email)

    return JsonResponse({'registerable':registerable, 'msg': message})

def logout_api(request):
    logout(request)
    return HttpResponseRedirect('/movie')

def download_api(request, movie_id):
    m = Movie.objects.get(pk=movie_id)
    u = request.user
    if(u.is_authenticated() and isUserOwn(u,m)):
        file = FileWrapper(open(m.movie_file.path, 'rb'))
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = str('attachment; filename='+m.movie_file.name)
        return response
    # Not return anything if client force to download without buy it

def rating_api(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    user = request.user
    rating_val = request.POST.get('rating', 0)
    if rating_val == '':
        rating_val = 0

    if Rating.objects.filter(movie=movie, user=user).exists():
        rating = Rating.objects.get(movie=movie, user=user)
        rating.rating = rating_val

    else:
        rating = Rating(movie=movie, user=user, rating=rating_val)

    rating.save()
    return HttpResponseRedirect('/movie/'+movie_id)


def does_serial_exist(code):
    for serial in Serial.objects.all():
        if (code == serial.serial_code):
            return True
    return False


def generate_code():
    serial = ''
    while True:
        for num in range(15):
            number = randint(1, 36)
            if (number <= 26):
                serial += chr(number + 96)
            else:
                serial += str(number - 27)
        if not does_serial_exist(serial):
            break
    return serial

def refillment_api(request):
    user = request.user
    if user.is_superuser:
        if(request.POST):
            if request.POST['price'] == '' or request.POST['amount'] == '':
                return TemplateResponse(request, 'refillment.html', {'error_msg': 'Please complete all information requested on this form.'})

            price = int(request.POST['price'])
            amount = int(request.POST['amount'])
            for i in range(0, amount):
                code = generate_code()
                serial = Serial.objects.create(serial_code=code, price=price)
            return TemplateResponse(request, 'refillment.html', {'success_admin_msg': 'Success! You have generated %d baht for %d serials.' % (price, amount)})
        return TemplateResponse(request, 'refillment.html')
    else:
        if (request.POST):
            code = request.POST['serial']
            price = 0

            if does_serial_exist(code):
                serial_obj = Serial.objects.get(serial_code = code)
                if serial_obj.is_active:
                    price = serial_obj.price
                    serial_obj.is_active = False
                    serial_obj.save()
                else:
                    message = "This serial code is not active or already in use."
                    return TemplateResponse(request, 'refillment.html', {'error_msg': message})

            else:
                message = "Invalid serial code, please try again"
                return TemplateResponse(request, 'refillment.html', {'error_msg': message})

            user_net = None
            if not Transaction.objects.filter(user = user).exists():
                user_net = UserNet.objects.create(user = user, net=0)
            else:
                user_net = UserNet.objects.get(user = user)
            Transaction.objects.create(user = user, price = price, net = user_net.net + price)
            user_net.net = user_net.net + price
            user_net.save()

            message = "You can check the refillment "
            return TemplateResponse(request, 'refillment.html', {'success_customer_msg': message})

        return TemplateResponse(request, 'refillment.html')

def transaction_api(request):
    records = Transaction.objects.filter(user=request.user)
    return TemplateResponse(request, 'transaction.html', {'records': records})

def buy_api(request, movie_id):
    if(request.POST):
        user = request.user
        userNet = UserNet.objects.get(user=user)
        movie = Movie.objects.get(pk=movie_id)
        userOwn = UserOwn.objects.filter(user=user, movie=movie)
        if(userOwn.exists()):
            request.session['error_msg'] = "Your already owned the movie."
            return redirect('movie:description', movie_id=movie_id)
        if((userNet.net < movie.movie_price)):
            request.session['error_msg'] = "Not enough money, please refill money or select an another movie."
            return redirect('movie:description', movie_id=movie_id)
        Transaction.objects.create(user = user, price = -movie.movie_price, net = userNet.net - movie.movie_price)
        UserOwn.objects.create(user = user, movie = movie)
        request.session['success_msg'] = "You can check your purchased movies "
        return redirect('movie:description', movie_id=movie_id)
    return redirect('movie:description', movie_id=movie_id)

class LibraryView(View):
    form_class = UserForm
    template_name = 'library.html'

    def get(self,request):
        list_own_movies = []
        user = request.user
        user_own = UserOwn.objects.filter(user=user)

        for own_movie in user_own:
            list_own_movies.append(own_movie.movie)

        return TemplateResponse(request, 'library.html',{'list_own_movies':list_own_movies})

class IndexView(View):
    form_class = UserForm
    template_name = 'index.html'

    def get(self, request):
        list_movies = {}
        all_movies = Movie.objects.all()[:4]
        all_genres = Genre.objects.all()
        rating_dict = {}

        for genre in all_genres:
            movie_in_genre = Movie.objects.filter(genre=genre)[:4]
            list_movies[genre] = movie_in_genre
            # list_movies.append(movie_in_genre)

        return TemplateResponse(request,'index.html',{'all_movies':all_movies,'all_genres':all_genres, 'list_movies':list_movies})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return TemplateResponse(request, self.template_name, {'form': form})

        return TemplateResponse(request, self.template_name, {'form': form, 'invalid_register': True})


class DescriptionView(View):
    form_class = UserForm
    template_name = 'description.html'

    def get(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
        movie.movie_teaser_url = self.convertLink(movie.movie_teaser_url)
        error_msg = request.session.get('error_msg')
        success_msg = request.session.get('success_msg')
        request.session['error_msg'] = None
        request.session['success_msg'] = None
        own = False
        if(request.user.is_authenticated() and UserOwn.objects.filter(user=request.user,movie=movie).exists()):
            own= True

        return TemplateResponse(request, 'description.html',{ 'movie':movie, 'rating': rating, 'own':own, 'error_msg': error_msg, 'success_msg': success_msg })

    def convertLink(self, link):
        str = link
        return str.replace('watch?v=', 'embed/')

class PolicyView(View):
    form_class = UserForm
    template_name = 'privacypolicy.html'

    def get(self, request):
        return TemplateResponse(request, self.template_name)

def isUserOwn(user,movie):
    user_owns = UserOwn.objects.filter(user=user,movie=movie)
    if user_owns.exists():
        return True
    return False
