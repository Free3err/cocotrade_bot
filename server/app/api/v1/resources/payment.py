from flask import request, make_response
from flask_restx import Resource

from server.app.api.v1.services import PaymentService


class PaymentStatic(Resource):
    @staticmethod
    def get(payment_id):
        payment = PaymentService.get_payment(payment_id)
        if payment:
            return make_response(
                {"ok": True, "data": payment}, 200)
        return make_response({"ok": False, "message": "No enough payment has found"}, 404)


class PaymentCreate(Resource):
    @staticmethod
    def post():
        body = request.json
        payment = PaymentService(body)

        if payment:
            return make_response(
                {"ok": True, "data": dict(payment.get())}, 200)
        return make_response({"ok": False, "message": "Something went wrong"}, 502)
