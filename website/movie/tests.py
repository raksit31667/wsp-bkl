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

class BKLLiveTestCase(LiveServerTestCase):

    # setUp is where you setup call fixture creation scripts
    # and instantiate the WebDriver, which in turns loads up the browser.
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(BKLTestCase, self).setUp()

    # Don't forget to call quit on your webdriver, so that
    # the browser is closed after the tests are ran
    def tearDown(self):
        time.sleep(2)
        self.selenium.quit()
        super(BKLTestCase, self).tearDown()

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

        username.send_keys('samakgame')
        password.send_keys('1234')

        submit.click()
        # TODO: assert the satisfied result
