# Create your tests here.

import pytest
from django.test import Client
from django.urls import reverse


#=============== VIEWS GET TESTS ===========
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

