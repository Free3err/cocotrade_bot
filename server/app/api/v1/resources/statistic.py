from flask import make_response
from flask_restx import Resource

from server.app.instance.db.handlers import DonationsHandler, FarmHandler, UserHandler
from server.app.utils import DatabaseUtils


class Statistic(Resource):
    @staticmethod
    def get():
        donations = DonationsHandler.get_all()
        farms = FarmHandler.get_all()
        users = UserHandler.get_all()

        donations_sum = 0
        coconuts_count = 0
        farms_count = 0

        if donations:
            donations_sum = sum([DatabaseUtils.object_to_dict(donation)['amount'] for donation in donations])
        if farms:
            farms_count = len([DatabaseUtils.object_to_dict(farm) for farm in farms])
        if users:
            coconuts_count = sum(
                [user.full_data()['coconut_balance'] + user.full_data()['farm']['uncollected'] for user in users])

        return make_response({'ok': True,
                              'data': {'coconuts_count': coconuts_count, 'farms_count': farms_count,
                                       'donations_sum': donations_sum}}, 200)
