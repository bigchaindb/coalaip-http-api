from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb.plugin import Plugin
from web.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

manifestation_views = Blueprint('manifestation_views', __name__)
manifestation_api = Api(manifestation_views)


def parse_model(required_fields):
    def _parse_model(inputs):
        for field in required_fields:
            try:
                value = inputs[field]
            except KeyError:
                raise KeyError('`{}` must be provided'.format(field))
            if bool(value) is not True:
                raise ValueError("`{}`'s value must be defined")
        return inputs
    return _parse_model


class ManifestationApi(Resource):
    def post(self):
        manifestation_model = parse_model(['name', 'datePublished', 'url'])
        work_model = parse_model(['name', 'author'])
        user_model = parse_model(['verifyingKey', 'signingKey'])

        parser = reqparse.RequestParser()
        parser.add_argument('manifestation', type=manifestation_model,
                            required=True, location='json')
        parser.add_argument('copyright_holder', type=work_model, required=True,
                            location='json')
        parser.add_argument('user', type=user_model, required=True,
                            location='json')
        args = parser.parse_args()

        manifestation = args['manifestation']
        work = args['work']

        copyright_holder = args['copyright_holder']
        copyright_holder['verifying_key'] = copyright_holder.pop('verifyingKey')
        copyright_holder['signing_key'] = copyright_holder.pop('signingKey')

        copyright, manifestation, work = coalaip.register_manifestation(
            manifestation_data=manifestation,
            copyright_holder=copyright_holder,
            work_data=work)

        res = {
            'manifestation': manifestation.to_jsonld(),
            'work': work.to_jsonld(),
            'copyright': copyright.to_jsonld()
        }

        return res


manifestation_api.add_resource(ManifestationApi, '/manifestations', strict_slashes=False)
