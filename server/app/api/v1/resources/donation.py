from flask import request, make_response
from flask_restx import Resource

from server.app.instance.db.handlers import DonationsHandler
from server.app.utils import DatabaseUtils


class DonationStatic(Resource):
    @staticmethod
    def get():
        pass


class DonationCreate(Resource):
    @staticmethod
    def post():
        body = request.json
        donation = DonationsHandler.create(donator_id=body['donator_id'], amount=body['amount'])
        if donation:
            donation_data = DatabaseUtils.object_to_dict(donation)
            return make_response({"ok": True, "data": donation_data}, 200)
        return make_response({"ok": False, "message": "Something went wrong while creating donation"}, 502)
