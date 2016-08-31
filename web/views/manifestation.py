from flask import request, Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp
from coalaip_bigchaindb.plugin import Plugin
from web.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

manifestation_views = Blueprint('manifestation_views', __name__)
manifestation_api = Api(manifestation_views)


class ManifestationApi(Resource):
    def post(self):
        data = request.get_json(force=True)
        manifestation = data['manifestation']
        work = data['work']

        user = data['user']
        user['verifying_key'] = user.pop('verifyingKey')
        user['signing_key'] = user.pop('signingKey')

        copyright, manifestation, work = coalaip.register_manifestation(
            manifestation_data=manifestation,
            user=user,
            work_data=work)

        res = {
            'manifestation': manifestation.to_jsonld(),
            'work': work.to_jsonld(),
            'copyright': copyright.to_jsonld()
        }

        return res


manifestation_api.add_resource(ManifestationApi, '/manifestations', strict_slashes=False)
