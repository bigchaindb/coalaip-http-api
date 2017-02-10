import json

from flask import url_for


def test_create_user(client):
    resp = client.post(url_for('user_views.userapi'))
    assert resp.status_code == 200
    assert resp.json['publicKey']
    assert resp.json['privateKey']


def test_create_manifestation(client, alice):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyrightHolder': alice,
        'work': {
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
    }

    expected = {
        'work': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'AbstractWork',
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
        'manifestation': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'CreativeWork',
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyright': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'Copyright',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    resp_dict = resp.json
    copyright_ = resp_dict['copyright']
    manifestation = resp_dict['manifestation']
    work = resp_dict['work']

    assert bool(copyright_['rightsOf']) is True
    assert bool(manifestation['manifestationOfWork']) is True

    # Check @ids
    assert copyright_['@id'].startswith('../rights/')
    assert bool(copyright_['@id'].strip('../rights/')) is True
    assert bool(manifestation['@id']) is True
    assert work['@id'].startswith('../works/')
    assert bool(work['@id'].strip('../works/')) is True

    resp_dict['copyright'].pop('rightsOf')
    resp_dict['manifestation'].pop('manifestationOfWork')
    resp_dict['copyright'].pop('@id')
    resp_dict['manifestation'].pop('@id')
    resp_dict['work'].pop('@id')
    assert resp_dict == expected
    assert resp.status_code == 200


def test_create_manifestation_missing_single_attribute(client, alice):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyrightHolder': alice,
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


def test_create_manifestation_missing_argument_in_body(client):
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


def test_create_right(client, alice, created_manifestation_resp):
    copyright_id = created_manifestation_resp['copyright']['@id']
    copyright_id = copyright_id.split('../rights/')[1]

    payload = {
        'currentHolder': alice,
        'right': {
            'license': 'http://www.ascribe.io/terms',
        },
        'sourceRightId': copyright_id,
    }

    expected = {
        'right': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'Right',
            'source': payload['sourceRightId'],
            'license': 'http://www.ascribe.io/terms',
        },
    }

    resp = client.post(url_for('right_views.rightapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    resp_dict = resp.json
    assert bool(resp_dict['right']['@id']) is True

    resp_dict['right'].pop('@id')
    assert resp_dict == expected
    assert resp.status_code == 200


def test_create_right_missing_single_attribute(client, alice):
    payload = {
        'currentHolder': alice,
        'right': {
            'notALicense': 'this is not a license',
        },
        'sourceRightId': 'mockId',
    }
    resp = client.post(url_for('right_views.rightapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400
    assert resp.json['message']['right'] == \
        "'`license` must be provided'"


def test_create_right_missing_argument_in_body(client, alice):
    payload = {
        'currentHolder': alice,
        'right': {
            'license': 'http://www.ascribe.io/terms',
        },
    }
    resp = client.post(url_for('right_views.rightapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400
    assert resp.json['message']['sourceRightId'] == \
        'Missing required parameter in the JSON body'


def test_transfer_right(client, alice, bob, carly, created_derived_right):
    payload = {
        'rightId': created_derived_right['@id'],
        'rightsAssignment': {
            'action': 'loan',
        },
        'currentHolder': alice,
        'to': {
            'publicKey': bob['publicKey'],
            'privateKey': None,
        }
    }

    expected = {
        'rightsAssignment': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'RightsTransferAction',
            '@id': '',
            'action': 'loan',
        },
    }

    resp = client.post(url_for('right_views.righttransferapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200
    assert resp.json == expected


def test_retransferred_right(client, bob, carly, transferred_derived_right):
    retransfer_payload = {
        'rightId': transferred_derived_right['@id'],
        'rightsAssignment': {
            'action': 'reloan',
        },
        'currentHolder': bob,
        'to': {
            'publicKey': carly['publicKey'],
            'privateKey': None,
        }
    }

    retransfer_expected = {
        'rightsAssignment': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'RightsTransferAction',
            '@id': '',
            'action': 'reloan',
        },
    }

    resp = client.post(url_for('right_views.righttransferapi'),
                       data=json.dumps(retransfer_payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200
    assert resp.json == retransfer_expected


def test_right_history(client, alice, bob, carly, retransferred_derived_right):
    right_id = retransferred_derived_right['@id']
    resp = client.get(
        url_for('right_views.righthistoryapi', right_id=right_id))
    assert resp.status_code == 200
    assert resp.json[0]['user']['publicKey'] == alice['publicKey']
    assert resp.json[1]['user']['publicKey'] == bob['publicKey']
    assert resp.json[2]['user']['publicKey'] == carly['publicKey']

    # First transaction should be the CREATE transaction
    assert resp.json[0]['eventId'] == right_id
