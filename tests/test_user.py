import pytest
from django.urls import reverse
from faker import Faker
from django.test import TestCase, Client
from users.models import User
from users.views import disable_user

fake = Faker()


@pytest.fixture
def user_creation_data():
    return User(
        username=fake.user_name(),
        email=fake.email(),
        name=fake.first_name(),
        last_name=fake.last_name(),
        password=fake.password(),

    )


@pytest.mark.django_db
def test_user_creation(user_creation_data):
    user_creation_data.is_staff = False
    user_creation_data.save()
    assert user_creation_data.is_staff == False


@pytest.mark.django_db
def test_superuser_creation(user_creation_data):
    user_creation_data.is_superuser = True
    user_creation_data.is_staff = True
    user_creation_data.save()
    assert user_creation_data.is_superuser == True




