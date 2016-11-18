from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create your tests here.

class BKLTestCase(LiveServerTestCase):

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
