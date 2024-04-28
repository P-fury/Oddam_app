# Create your tests here.

import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import user
from oddam_app.conftest import create_user
from user.models import CustomUser


# =============== VIEWS GET TESTS ===========
@pytest.mark.django_db
def test_index_get():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_get():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_get():
    client = Client()
    url = reverse('logout')
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_adddonation_get():
    client = Client()
    url = reverse('adddonation')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_confirm_get():
    client = Client()
    url = reverse('confirm')
    response = client.get(url)
    assert response.status_code == 200


# ======== LOGIN USER_EDIT ==========
@pytest.mark.django_db
def test_user_edit_get(create_user):
    client = Client()
    client.force_login(create_user)
    url = reverse('user_edit')
    response = client.get(url)
    assert response.context['user'] == create_user
    assert response.status_code == 200


class selenium_button_tests(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.user = CustomUser.objects.create_user(email='fix@email.com', password='test123@A', first_name='test_first',
                                                   last_name='test_last', username='test_normal', is_active=True)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get(self.live_server_url + '/login/')
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Zaloguj')]")
        login_form = self.driver.find_element(By.NAME, "email")
        login_password = self.driver.find_element(By.NAME, "password")
        login_form.send_keys(self.user.email)
        login_password.send_keys('test123@A')
        login_button.click()
        logged_text = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f"//li[contains(@class, 'logged') and contains(@class, 'user')]")
            )
        )
        assert logged_text.text == F'Witaj {self.user.first_name}'
        donation_button = self.driver.find_element(By.LINK_TEXT, "Przekaż dary")
        donation_button.click()

