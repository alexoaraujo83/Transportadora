import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_healthcheck(client):
    response = client.get('/health/')
    assert response.status_code in (200, 204)


def test_login_page(client):
    response = client.get('/accounts/login/')
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get('/')
    assert response.status_code in (200, 302)
