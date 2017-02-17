from web.server import create_app

from flask import url_for
import pytest


@pytest.fixture
def app():
    app = create_app({'debug': True})
    return app


@pytest.fixture
def user(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def created_manifestation_resp(client, user):
    import json
    from time import sleep
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyrightHolder': user,
        'work': {
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
    }

    resp = client.post(url_for('manifestation_views.manifestationapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return resp.json
