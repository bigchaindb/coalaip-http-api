from flask import Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb import Plugin
from web.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

user_views = Blueprint('user_views', __name__)
user_api = Api(user_views)


class UserApi(Resource):
    def post(self):
        """API endpoint to create a new keypair for a user

        Return:
            A dict containing the publicKey and privateKey.
        """
        # TODO FOR COALA IP: Return CamelCase key names
        user = coalaip.generate_user()
        # TODO: We might want to have a generic function for this at one point.
        user['publicKey'] = user.pop('public_key')
        user['privateKey'] = user.pop('private_key')
        return user


user_api.add_resource(UserApi, '/users', strict_slashes=False)
