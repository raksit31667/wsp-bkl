from django.test import TestCase, LiveServerTestCase, RequestFactory, Client
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import Genre, Movie, Rating, Serial, Transaction, UserNet, UserOwn

import json, time

from .views import filter, search_movie, login_api, refillment_api, buy_api

# Create your tests here.

class BKLLiveTestCase(LiveServerTestCase):

    # setUp is where you setup call fixture creation scripts
    # and instantiate the WebDriver, which in turns loads up the browser.
    def setUp(self):
        self.selenium = WebDriver()
        super(BKLLiveTestCase, self).setUp()

    # Don't forget to call quit on your webdriver, so that
    # the browser is closed after the tests are ran
    def tearDown(self):
        time.sleep(2)
        self.selenium.quit()
        super(BKLLiveTestCase, self).tearDown()

    def test_login(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/movie')
        login_nav = selenium.find_element_by_link_text('Login')
        login_nav.click()
        username = selenium.find_element_by_id('login-username')
        password = selenium.find_element_by_id('login-password')
        error_message = selenium.find_element_by_id('login-error-message')
        submit = selenium.find_element_by_xpath("//*[contains(text(), 'Sign in')]")

        # need to wait until login modal is visible
        time.sleep(2)

        username.send_keys('admin')
        password.send_keys('correct')
        submit.click()

        # need to wait login process
        time.sleep(1)

        self.assertEqual(error_message.text, "Invalid username or password.")

        username.clear()
        password.clear()

        username.send_keys('admin')
        password.send_keys('incorrect')
        submit.click()

        # TODO: assert the satisfied result

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/movie')
        register_nav = selenium.find_element_by_link_text('Register')
        register_nav.click()
        username = selenium.find_element_by_id('register-username')
        email = selenium.find_element_by_id('register-email')
        password = selenium.find_element_by_id('register-password')
        confirm_password = selenium.find_element_by_id('register-password-confirm')
        check_policy = selenium.find_element_by_id('register-policy')
        error_message = selenium.find_element_by_id('register-error-message')
        submit = selenium.find_element_by_xpath("//*[contains(text(), 'Create Account')]")

        # need to wait until register modal is visible
        time.sleep(2)

        username.send_keys('bkltestcase')
        email.send_keys('bkltestcase@hotmail.com')
        password.send_keys('password')
        confirm_password.send_keys('drowssap')
        check_policy.click()
        submit.click()

        # need to wait register process
        time.sleep(1)

        self.assertEqual(error_message.text, "Passwords are not the same.")

        username.clear()
        email.clear()
        password.clear()
        confirm_password.clear()
        check_policy.click()

        username.send_keys('bkltestcase')

        # email.send_keys('bkltestcase@hotmail.com')
        password.send_keys('password')
        confirm_password.send_keys('password')
        check_policy.click()
        submit.click()

        # need to wait register process
        time.sleep(1)

        self.assertEqual(error_message.text, "Please complete all information requested on this form.")
        username.clear()
        email.clear()
        password.clear()
        confirm_password.clear()
        check_policy.click()

        username.send_keys('bkltestcase')
        email.send_keys('bkltestcase@hotmail.com')
        password.send_keys('password')
        confirm_password.send_keys('password')

        # check_policy.click()
        submit.click()

        # need to wait register process
        time.sleep(1)

        self.assertEqual(error_message.text, "Please accept our policy.")


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

    def test_refillment(self):
        request = self.factory.get('/')
        num_serials_before = 0
        request.user = self.test_admin

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['price'] = ''
        request.POST['amount'] = ''
        request.POST._mutable = mutable

        response = refillment_api(request)
        expected = 'Please complete all information requested on this form.'
        result = response.context_data['error_msg']
        self.assertEqual(expected, result)

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['price'] = '100'
        request.POST['amount'] = '5'
        request.POST._mutable = mutable

        response = refillment_api(request)
        num_serials_after = len(Serial.objects.all())

        expected = 'Success! You have generated 100 baht for 5 serials.'
        result = response.context_data['success_admin_msg']
        self.assertEqual(num_serials_before + 5, num_serials_after)
        self.assertEqual(expected, result)

        request = self.factory.get('/')
        request.user = self.test_user1

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['serial'] = ''
        request.POST._mutable = mutable

        response = refillment_api(request)
        expected = 'Invalid serial code, please try again'
        result = response.context_data['error_msg']
        self.assertEqual(expected, result)

        request = self.factory.get('/')
        request.user = self.test_user1

        test_serial = Serial.objects.get(pk=1).serial_code
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['serial'] = test_serial
        request.POST._mutable = mutable

        response = refillment_api(request)
        expected = 'You can check the refillment '
        result = response.context_data['success_customer_msg']
        self.assertEqual(expected, result)

        request = self.factory.get('/')
        request.user = self.test_user1

        test_serial = Serial.objects.get(pk=1).serial_code
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['serial'] = test_serial
        request.POST._mutable = mutable

        response = refillment_api(request)
        expected = 'This serial code is not active or already in use.'
        result = response.context_data['error_msg']
        self.assertEqual(expected, result)

    def test_buy(self):
        request = self.factory.get('/')
        request.user = self.test_user1
        response = buy_api(request, 2)
        expected = 0
        user_own = UserOwn.objects.filter(movie=self.test_movie2)
        self.assertEqual(expected, len(user_own))

        UserNet.objects.create(user=self.test_user1, net=100)

        # Annotate a request object with a session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = buy_api(request, 1)
        expected = 0
        user_own = UserOwn.objects.filter(movie=self.test_movie1)
        self.assertEqual(expected, len(user_own))

        expected_net = 50
        user_net = UserNet.objects.get(user=self.test_user1)
        result_net = user_net.net - self.test_movie2.movie_price
        self.assertEqual(50, result_net)
