from flask import make_response
from flask_restx import Resource

from server.app.instance.db.handlers.locations import LocationHandler
from server.app.utils import DatabaseUtils


class Location(Resource):
    @staticmethod
    def get(location_id):
        location = LocationHandler.get(location_id=location_id)
        if location:
            location_data = DatabaseUtils.object_to_dict(location)
            return make_response({"ok": True, "data": location_data}, 200)
        return make_response({"ok": False, "data": None}, 404)