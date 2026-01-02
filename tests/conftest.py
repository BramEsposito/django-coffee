"""
Pytest configuration and fixtures for django-coffee-admin tests
"""
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory


@pytest.fixture
def request_factory():
    """Fixture to provide Django RequestFactory"""
    return RequestFactory()


@pytest.fixture
def staff_user(db):
    """Fixture to create a staff user"""
    user = User.objects.create_user(
        username='staffuser',
        email='staff@example.com',
        password='testpass123',
        is_staff=True,
        is_active=True
    )
    return user


@pytest.fixture
def superuser(db):
    """Fixture to create a superuser"""
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    return user


@pytest.fixture
def regular_user(db):
    """Fixture to create a regular (non-staff) user"""
    user = User.objects.create_user(
        username='regularuser',
        email='user@example.com',
        password='userpass123',
        is_staff=False,
        is_active=True
    )
    return user


@pytest.fixture
def authenticated_staff_request(request_factory, staff_user):
    """Fixture to provide an authenticated staff request"""
    request = request_factory.get('/')
    request.user = staff_user
    return request


@pytest.fixture
def authenticated_superuser_request(request_factory, superuser):
    """Fixture to provide an authenticated superuser request"""
    request = request_factory.get('/')
    request.user = superuser
    return request


@pytest.fixture
def authenticated_regular_request(request_factory, regular_user):
    """Fixture to provide an authenticated regular user request"""
    request = request_factory.get('/')
    request.user = regular_user
    return request
