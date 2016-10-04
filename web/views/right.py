from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb import Plugin
from web.utils import get_bigchaindb_api_url, parse_model


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

right_views = Blueprint('right_views', __name__)
right_api = Api(right_views)


class RightApi(Resource):
    def post(self):
        """API endpoint to attach a Right to a Manifestation or another Right
        """
        user_model = parse_model(['verifyingKey', 'signingKey'])
        right_model = parse_model(['rightsOf', 'license'])

        parser = reqparse.RequestParser()
        parser.add_argument('right', type=right_model,
                            required=True, location='json')
        parser.add_argument('user', type=user_model, required=True,
                            location='json')

        args = parser.parse_args()
        right = args['right']
        user = args['user']

        right = coalaip.derive_right(right_data=right, current_holder=user)

        return right.to_jsonld()


right_api.add_resource(RightApi, '/rights', strict_slashes=False)
