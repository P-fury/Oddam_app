# Create your tests here.
import time

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
from oddam_app.models import Institution, Category, Donation
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


# ========== CREATING USER ===========
@pytest.mark.django_db
def test_user_create():
    client = Client()
    url = reverse('register')
    data = {
        'first_name': 'Pitest',
        'last_name': 'Lastest',
        'email': 'email@test.pl',
        'password1': 'ValidPassword123!',
        'password2': 'ValidPassword123!',
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    user_exists = CustomUser.objects.filter(first_name='Pitest').exists()
    assert user_exists


@pytest.mark.django_db
def test_user_edit_first_and_last_name_(create_user):
    client = Client()
    client.force_login(create_user)
    url = reverse('user_edit')
    data = {
        'edit_data': '',
        'first_name': 'NewTestName',
        'last_name': 'NewTestLastName',
        'confirm-password': 'test123',
        'email': 'fix@email.com'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    user_exists = CustomUser.objects.filter(first_name='NewTestName').exists()
    assert user_exists
    assert CustomUser.objects.filter(email='fix@email.com')

# class selenium_button_tests(StaticLiveServerTestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.maximize_window()
#         self.user = CustomUser.objects.create_user(email='fix@email.com', password='test123@A', first_name='test_first',
#                                                    last_name='test_last', username='test_normal', is_active=True)
#         self.institution = Institution.objects.create(name='selenium_test_inst', description='inst for selenium test',
#                                                       type='fundacja')
#         self.institution2 = Institution.objects.create(name='selenium_test_inst2',
#                                                        description='inst2 for selenium test',
#                                                        type='organizacja_pozarządowa')
#         self.categories = {}
#         for i in range(4):
#             self.categories[f'category{i}'] = Category.objects.create(name=f'selenium_test_category{i}')
#         self.institution.categories.add(self.categories['category1'])
#         self.institution2.categories.add(self.categories['category1'])
#
#     def tearDown(self):
#         time.sleep(0)
#         webdriver.Chrome().quit()
#
#     def test_login(self):
#         self.driver.get(self.live_server_url + '/login/')
#         login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Zaloguj')]")
#         login_form = self.driver.find_element(By.NAME, "email")
#         login_password = self.driver.find_element(By.NAME, "password")
#         login_form.send_keys(self.user.email)
#         login_password.send_keys('test123@A')
#         login_button.click()
#         logged_text = WebDriverWait(self.driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH,
#                  f"//li[contains(@class, 'logged') and contains(@class, 'user')]")
#             )
#         )
#         assert logged_text.text == F'Witaj {self.user.first_name}'
#         donation_button = self.driver.find_element(By.LINK_TEXT, "Przekaż dary")
#         donation_button.click()
#         checkbox_span = self.driver.find_element(By.XPATH,
#                                                  "//label[input[@type='checkbox'][@value='selenium_test_category1']]/span[@class='checkbox']")
#         checkbox_span.click()
#         next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Dalej')]")
#         next_button.click()
#         input_bags = self.driver.find_element(By.NAME, 'bags')
#         input_bags.clear()
#         input_bags.send_keys('66')
#         next_button = self.driver.find_element(By.CSS_SELECTOR, "div[data-step='2'] .btn.next-step")
#         next_button.click()
#         span_element = self.driver.find_element(By.XPATH, "//label[input[@value='2']]/span[@class='checkbox radio']")
#         span_element.click()
#         next_button = self.driver.find_element(By.CSS_SELECTOR, "div[data-step='3'] .btn.next-step")
#         next_button.click()
#         street_name = self.driver.find_element(By.XPATH, "//input[@name='address']")
#         city_name = self.driver.find_element(By.XPATH, "//input[@name='city']")
#         post_code = self.driver.find_element(By.XPATH, "//input[@name='postcode']")
#         phone_number = self.driver.find_element(By.XPATH, "//input[@name='phone']")
#         date = self.driver.find_element(By.XPATH, "//input[@name='data']")
#         time = self.driver.find_element(By.XPATH, "//input[@name='time']")
#         more_info = self.driver.find_element(By.XPATH, "//textarea[@name='more_info']")
#
#         street_name.send_keys('selenium_street')
#         city_name_text = 'selenium_city'
#         city_name.send_keys(city_name_text)
#         post_code.send_keys('44-233')
#         phone_number.send_keys('324-322-322')
#         date.send_keys('12/12/1989')
#         time.send_keys('15:45')
#         more_info.send_keys('No more info')
#
#         next_button = self.driver.find_element(By.CSS_SELECTOR, "div[data-step='4'] .btn.next-step")
#         next_button.click()
#
#         confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Potwierdzam')]")
#         confirm_button.click()
#
#         assert Donation.objects.count() == 1
#         test_donation = Donation.objects.last()
#         assert test_donation.institution_id == self.institution2.id
#         assert self.categories['category1'] in test_donation.category.all()
#         assert test_donation.city == city_name_text
