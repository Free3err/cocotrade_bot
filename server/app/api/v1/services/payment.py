import uuid

from yookassa import Payment
from yookassa.domain.exceptions import NotFoundError


class PaymentService:
    def __init__(self, data: dict) -> None:
        payment_uuid = uuid.uuid4()
        self.payment = Payment.create({
            "amount": {
                "value": data["amount"],
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "confirmation_url": f"https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId={payment_uuid}",
                "return_url": f"https://t.me/cocotrade_bot"
            },
            "capture": True,
            "description": data["description"],
            "metadata": {
                "telegram_id": data["telegram_id"],
                "is_donate": data["is_donate"]
            }}, payment_uuid)

    def get(self):
        return self.payment

    @staticmethod
    def get_payment(payment_uuid):
        try:
            payment = dict(Payment.find_one(payment_uuid))
            return payment
        except NotFoundError:
            return None
