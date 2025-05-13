from yookassa import Payment

from .resources import *

resources = {
    User: '/api/v1/user/<int:telegram_id>',
    UserList: '/api/v1/users',
    TechnologyList: '/api/v1/technologies',
    Statistic: '/api/v1/statistic',
    CoconutList: '/api/v1/coconuts',
    PaymentStatic: '/api/v1/payment/<string:payment_id>',
    PaymentCreate: '/api/v1/payment',
    DonationStatic: '/api/v1/donation/<int:donation_id>',
    DonationCreate: '/api/v1/donation',
}


def register_resources(api):
    for resource, path in resources.items():
        api.add_resource(resource, path)
