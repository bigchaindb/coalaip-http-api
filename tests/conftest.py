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


@pytest.fixture
def carly(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def created_derived_right_with_mock_source(client, alice):
    import json
    from time import sleep

    payload = {
        'currentHolder': alice,
        'right': {
            'license': 'http://www.ascribe.io/terms',
        },
        'sourceRightId': 'mockId',
    }

    resp = client.post(url_for('right_views.rightapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return resp.json['right']
