"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation on ReadTheDocs:
 - https://bigchaindb.readthedocs.io/en/latest/drivers-clients/http-client-server-api.html
"""
from flask import current_app, Blueprint
from flask_restful import Resource, Api, reqparse

from coalaip_bigchaindb.plugin import Plugin
from coalaip import bind_plugin

from web.views.base import make_error


coalaip_plugin = bind_plugin(Plugin)

manifestation_views = Blueprint('manifestation_views', __name__)
manifestation_api = Api(manifestation_views)


class ManifestationApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('')

    def post(self):
        """API endpoint to register a coalaip manifestation.

        Return:
            A dict containing the data about the transaction.
        """
        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            tx = bigchain.get_transaction(tx_id)

        if not tx:
            return make_error(404)

        return tx


manifestation_api.add_resource(ManifestationApi, '/manifestations', strict_slashes=False)
