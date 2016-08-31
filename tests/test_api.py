from flask import url_for


def test_create_manifestation(app, client):
    resp = client.post(url_for('manifestation_views.manifestationapi'))
    assert resp.json == {'hello': 'world'}
