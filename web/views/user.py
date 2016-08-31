from flask import Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb import Plugin


coalaip = CoalaIp(Plugin('http://localhost:9984/'))

user_views = Blueprint('user_views', __name__)
user_api = Api(user_views)


class UserApi(Resource):
    def post(self):
        """API endpoint to create a new keypair for a user

        Return:
            A dict containing the verifying_key and signing_key.
        """
        # TODO FOR COALA IP: Return CamelCase key names
        user = coalaip.generate_user()
        # TODO: We might want to have a generic function for this at one point.
        user['verifyingKey'] = user.pop('verifying_key')
        user['signingKey'] = user.pop('signing_key')
        return user


user_api.add_resource(UserApi, '/users', strict_slashes=False)
