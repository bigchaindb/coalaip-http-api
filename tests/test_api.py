from flask import url_for


def test_create_manifestation(client):
    resp = client.post(url_for('manifestation_views.manifestationapi'))
    assert resp.json == {'hello': 'world'}


def test_create_user(client):
    resp = client.post(url_for('user_views.userapi'))
    assert resp.json['verifyingKey']
    assert resp.json['signingKey']
