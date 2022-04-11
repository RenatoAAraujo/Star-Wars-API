"""Star Wars integration endpoints"""
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.star_wars import star_wars_api
from app.star_wars.services.skywalker import skywalker_films
from app.star_wars.swagger.models import skywalker
from app.services.exceptions.errors import (
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)
from app.services.exceptions.swagger.models import error_model
from app.services.requests.helpers import default_return, request_default_filters

parser = star_wars_api.parser()
parser.add_argument("Authorization", location="headers")


@star_wars_api.route("/skywalker")
class StarWarsIntegration(Resource):
    """Star Wars integration route"""

    @star_wars_api.response(200, "Success", skywalker)
    @star_wars_api.response(400, "Bad Request", error_model)
    @star_wars_api.response(401, "Unauthorized", error_model)
    @star_wars_api.response(404, "Not Found", error_model)
    @star_wars_api.response(500, "Something went wrong", error_model)
    def get(self):
        """Get Skywalker lore"""
        try:
            item = {"status": 200}
            item.update(skywalker_films())

            return default_return(200, item)
        except (
            BadRequestError,
            InternalServerError,
            NotFoundError,
            UnauthorizedError,
        ) as e:
            return default_return(e.status_code, e.message)
        except Exception as e:
            return default_return(500, str(e))
