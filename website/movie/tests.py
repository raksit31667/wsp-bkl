from django.test import TestCase, LiveServerTestCase, Client
from django.core.files import File
from django.contrib.auth.models import User
from .models import Genre, Movie, Rating
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create your tests here.

class BKLTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user('bkl', 'bkl@ku.ac.th', 'password')
        test_genre = Genre.objects.create(genre_name="Test Genre", genre_description="This is the test genre.")
        test_movie = Movie.objects.create(genre=test_genre, movie_name="Test Movie", movie_description="This is the test movie.",
        release_year=1970, movie_price=150, movie_teaser_url="https://bkltestcase.ku.ac.th",
        movie_thumbnail="media/test/test.jpg", movie_file="media/test/test.mp4",
        user=test_user)

    def test_add_movie(self):
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 1)

    def test_description(self):
        movie = Movie.objects.get(movie_name="Test Movie")
        self.assertEqual(movie.movie_description, "This is the test movie.")

    def test_search(self):
        movies = Movie.objects.filter(movie_name__icontains='t')
        for movie in movies:
            self.assertEqual(movie.__str__(), "Test Movie (1970)")

class BKLLiveTestCase(LiveServerTestCase):

    # setUp is where you setup call fixture creation scripts
    # and instantiate the WebDriver, which in turns loads up the browser.
    def setUp(self):
        self.selenium = webdriver.Chrome()
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
        submit = selenium.find_element_by_xpath("//*[contains(text(), 'Sign in')]")

        # need to wait until login modal is visible
        time.sleep(2)

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
        self.assertEqual(error_message.text, "Passwords are not the same")

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
        self.assertEqual(error_message.text, "Please input all the of fields")

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
        self.assertEqual(error_message.text, "Please accept our policy")
