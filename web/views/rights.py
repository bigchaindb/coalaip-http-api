from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb.plugin import Plugin
from web.models import right_model, user_model
from web.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

right_views = Blueprint('right_views', __name__)
right_api = Api(right_views)


class RightApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('right', type=right_model, required=True,
                            location='json')
        parser.add_argument('sourceRightId', type=str, required=True,
                            location='json')
        parser.add_argument('currentHolder', type=user_model, required=True,
                            location='json')
        args = parser.parse_args()

        source_right_id = args['sourceRightId']
        right = args['right']
        right['allowedBy'] = source_right_id

        current_holder = args['currentHolder']
        current_holder['verifying_key'] = current_holder.pop('verifyingKey')
        current_holder['signing_key'] = current_holder.pop('signingKey')

        right = coalaip.derive_right(right_data=right,
                                     current_holder=current_holder)

        right_jsonld = right.to_jsonld()
        right_jsonld['@id'] = right.persist_id
        res = {'right': right_jsonld}

        return res


right_api.add_resource(RightApi, '/rights', strict_slashes=False)
