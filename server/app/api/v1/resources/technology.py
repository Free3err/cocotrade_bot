from flask import make_response
from flask_restx import Resource

from server.app.instance.db.handlers import TechnologyHandler
from server.app.utils import DatabaseUtils


class TechnologyList(Resource):
    @staticmethod
    def get():
        technologies = TechnologyHandler.get_all()

        if technologies:
            technologies_datas = [DatabaseUtils.object_to_dict(tech) for tech in technologies]
            return make_response({'ok': True, 'data': technologies_datas}, 200)
        return make_response({'ok': False, 'message': "No enough technology has found"}, 404)
