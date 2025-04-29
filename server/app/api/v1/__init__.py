from .resources import *

resources = {
    User: '/api/v1/user/<int:telegram_id>',
    Location: '/api/v1/location/<int:location_id>',
}

def register_resources(api):
    for resource, path in resources.items():
        api.add_resource(resource, path)