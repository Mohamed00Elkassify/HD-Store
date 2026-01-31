import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="Password123!")


@pytest.fixture
def staff(db):
    u = User.objects.create_user(username="staff1", password="Password123!")
    u.is_staff = True
    u.save()
    return u


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def staff_client(api_client, staff):
    api_client.force_authenticate(user=staff)
    return api_client
