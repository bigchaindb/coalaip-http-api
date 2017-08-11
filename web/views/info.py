from flask import Blueprint
from flask_restful import Resource, Api


info_views = Blueprint('info_views', __name__)
info_api = Api(info_views)


class InfoApi(Resource):
    def get(self):
        return 'It works! Check the docs on how to use the API'


info_api.add_resource(InfoApi, '/', strict_slashes=False)
