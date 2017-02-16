from flask import Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from web.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

work_views = Blueprint('work_views', __name__)
work_api = Api(work_views)


class WorkApi(Resource):
    def get(self, entity_id):
        work = entities.Work.from_persist_id(
            entity_id, plugin=coalaip.plugin, force_load=True)
        return work.to_jsonld()


work_api.add_resource(WorkApi, '/work/<entity_id>', strict_slashes=False)
