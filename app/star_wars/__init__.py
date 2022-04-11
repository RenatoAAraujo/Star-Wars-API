"""Star wars namespace"""
from flask_restx import Namespace

from app.star_wars.swagger.models import skywalker

star_wars_api = Namespace("star_wars", description="Star Wars Endpoints")

# models
star_wars_api.models["skywalker"] = skywalker
