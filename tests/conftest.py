from web.server import create_app

from flask import url_for
import pytest


@pytest.fixture
def app():
    app = create_app({'debug': True})
    return app


@pytest.fixture
def alice(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def bob(client):
    return client.post(url_for('user_views.userapi')).json
