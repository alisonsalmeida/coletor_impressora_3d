from sanic import Blueprint
from .collect import collect_route


routes = Blueprint.group(collect_route)
