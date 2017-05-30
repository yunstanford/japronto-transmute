from transmute_core import TransmuteFunction, default_context
from .handler import create_handler


def add_route(app, fn, context=default_context):
	pass



def _convert_to_aiohttp_path(path):
    """ convert a transmute path to one supported by japronto. """
    return path
