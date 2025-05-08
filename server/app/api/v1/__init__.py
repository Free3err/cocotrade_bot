from .resources import *

resources = {
    User: '/api/v1/user/<int:telegram_id>',
    TechnologyList: '/api/v1/technologies',
}


def register_resources(api):
    for resource, path in resources.items():
        api.add_resource(resource, path)
