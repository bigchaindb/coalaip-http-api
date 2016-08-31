"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation on ReadTheDocs:
 - https://bigchaindb.readthedocs.io/en/latest/drivers-clients/http-client-server-api.html
"""
from flask import Blueprint
from flask_restful import Resource, Api

from coalaip_bigchaindb.plugin import Plugin
from coalaip import CoalaIp


manifestation_views = Blueprint('manifestation_views', __name__)
manifestation_api = Api(manifestation_views)


class ManifestationApi(Resource):
    def post(self):
        plugin = Plugin('http://localhost:9984')
        coala_ip = CoalaIp(plugin)
        return None


manifestation_api.add_resource(ManifestationApi, '/manifestations', strict_slashes=False)
