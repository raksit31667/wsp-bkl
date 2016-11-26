from django.test import TestCase, LiveServerTestCase, RequestFactory, Client
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.urlresolvers import reverse
from .models import Genre, Movie, Rating, Serial

import json

from .views import filter, search_movie, login_api, register_api

# Create your tests here.

class BKLTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.test_admin = User.objects.create_superuser('admin', 'admin@bkl.ku.ac.th', 'incorrect')

        self.test_user1 = User.objects.create_user('bkl', 'bkl@bkl.ku.ac.th', 'password')
        self.test_user2 = User.objects.create_user('bkl2', 'bkl2@bkl.ku.ac.th', 'password')

        self.test_genre1 = Genre.objects.create(genre_name="Test Genre 01", genre_description="This is the test genre.")
        self.test_genre2 = Genre.objects.create(genre_name="Test Genre 02", genre_description="This is the test genre.")

        self.test_movie1 = Movie.objects.create(genre=self.test_genre1, movie_name="Test Movie 01", movie_description="This is the test movie.",
        release_year=1970, movie_price=150, movie_teaser_url="https://bkltestcase.ku.ac.th",
        movie_thumbnail="test.jpg", movie_file="test.mp4",
        user=self.test_admin)

        self.test_movie2 = Movie.objects.create(genre=self.test_genre2, movie_name="Test Movie 02", movie_description="This is the test movie.",
        release_year=2016, movie_price=50, movie_teaser_url="https://bkltestcase.ku.ac.th",
        movie_thumbnail="test.jpg", movie_file="test.mp4",
        user=self.test_admin)

    def test_add_movie(self):
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 2)

    def test_description(self):
        movie = self.test_movie1
        self.assertEqual(movie.movie_description, "This is the test movie.")

    def test_search(self):
        request = self.factory.get('/')
        request.user = self.test_user1

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['typeahead'] = '01'
        request.POST._mutable = mutable

        response = search_movie(request)
        expected = Movie.objects.filter(movie_name__icontains='Test Movie 01')
        result = response.context_data['result']
        self.assertEqual(len(expected), len(result))

    def test_rating(self):
        movie = self.test_movie1
        rating_from_user = Rating.objects.create(movie=movie, user=self.test_user1, rating=2)
        rating_from_user2 = Rating.objects.create(movie=movie, user=self.test_user2, rating=3)
        self.assertEqual(movie.get_avg_rating(), 2.5)

    def test_filter(self):
        request = self.factory.get('/')
        request.user = self.test_admin
        genre = "Test Genre 01"
        sortby = "movie_name"
        response = filter(request, genre, sortby)
        expected = Movie.objects.filter(genre=self.test_genre1)
        result  = response.context_data['selected_movies']
        self.assertEqual(len(expected), len(result))

    def test_login(self):
        request = self.factory.get('/')

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = 'bkl'
        request.POST['password'] = 'incorrect'
        request.POST._mutable = mutable

        response = login_api(request)

        expected = 'Invalid username or password.'
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(expected, result['msg'])

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = 'bkl'
        request.POST['password'] = 'password'
        request.POST._mutable = mutable

        # Annotate a request object with a session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = login_api(request)
        expected = 'success'
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(expected, result['msg'])
