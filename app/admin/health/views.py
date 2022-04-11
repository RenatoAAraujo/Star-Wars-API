"""Health endpoints"""
from flask import current_app
from flask_restx import Resource

from app.admin.health import health_api
from app.admin.health.swagger.models import get_health
from app.services.exceptions.errors import InternalServerError
from app.services.exceptions.swagger.models import error_model
from app.services.requests.helpers import default_return


@health_api.route("")
class Health(Resource):
    """Health route"""

    @health_api.response(200, "Success", get_health)
    @health_api.response(500, "Something went wrong", error_model)
    def get(self):
        """Check API health"""
        try:
            return {"hash": current_app.config["APP_HASH"]}, 200
        except InternalServerError as e:
            return default_return(e.status_code, e.message)
        except Exception as e:
            return default_return(500, str(e))
