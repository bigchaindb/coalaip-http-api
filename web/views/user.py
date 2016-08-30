"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation on ReadTheDocs:
 - https://bigchaindb.readthedocs.io/en/latest/drivers-clients/http-client-server-api.html
"""
from flask import current_app, Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb import Plugin

from web.views.base import make_error


coalaip = CoalaIp(Plugin('http://localhost:9984/'))

user_views = Blueprint('user_views', __name__)
user_api = Api(user_views)


class UserApi(Resource):
    def post(self):
        """API endpoint to create a new keypair for a user

        Return:
            A dict containing the verifying_key and signing_key.
        """
        return coalaip.generate_user()._asdict()


user_api.add_resource(UserApi, '/users', strict_slashes=False)
