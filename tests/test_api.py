import json

from flask import url_for


def test_create_user(client):
    resp = client.post(url_for('user_views.userapi'))
    assert resp.status_code == 200
    assert resp.json['verifyingKey']
    assert resp.json['signingKey']


def test_create_manifestation(client, user):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyright_holder': user,
        'work': {
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
    }

    expected = {
        'work': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'CreativeWork',
            '@id': '',
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
        'manifestation': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'CreativeWork',
            '@id': '',
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
            'isManifestation': True,
        },
        'copyright': {
            '@context': '<coalaip placeholder>',
            '@type': 'Copyright',
            '@id': '',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    resp_dict = resp.json
    assert bool(resp_dict['copyright']['rightsOf']) is True
    assert bool(resp_dict['manifestation']['manifestationOfWork']) is True
    resp_dict['copyright'].pop('rightsOf')
    resp_dict['manifestation'].pop('manifestationOfWork')
    assert resp_dict == expected
    assert resp.status_code == 200


def test_create_manifestation_single_missing_param(client, user):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyright_holder': user,
        'work': {
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    # TODO: I really don't know why flask_restful includes the extra '' in the
    #       error message's response.
    assert resp.status_code == 400
    assert resp.json['message']['manifestation'] == \
        "'`datePublished` must be provided'"


def test_create_manifestation_missing_body(client, user):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'url': 'http://localhost/lordoftherings.txt',
            'datePublished': '29-07-1954',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400
    assert resp.json['message']['work'] == \
        'Missing required parameter in the JSON body'
