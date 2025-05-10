from flask import make_response
from flask_restx import Resource

from server.app.instance.db.handlers import CoconutHandler
from server.app.utils import DatabaseUtils


class CoconutList(Resource):
    @staticmethod
    def get():
        coconuts = CoconutHandler.get_all()

        if coconuts:
            coconuts_datas = [DatabaseUtils.object_to_dict(coco) for coco in coconuts]
            return make_response({"ok": True, "data": coconuts_datas})
        return make_response({"ok": False, "message": "No enough coconuts has found"})
