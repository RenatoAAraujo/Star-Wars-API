"""Custom error classes"""

import logging
import sqlalchemy

from flask import jsonify, make_response
from http import HTTPStatus

from app import jwt
from app.services.exceptions import exception_handler_bp

logger = logging.getLogger(__name__)


class BadRequestError(Exception):
    """Exception raised for status 400 (Bad Request)."""

    def __init__(self, message="Bad Request"):
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Exception raised for status 401 (Unauthorized)."""

    def __init__(self, message="Unauthorized"):
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    """Exception raised for status 403 (Forbidden)."""

    def __init__(self, message="Forbidden"):
        self.status_code = HTTPStatus.FORBIDDEN
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exception raised for status 404 (Not Found)."""

    def __init__(self, message="Not Found"):
        self.status_code = HTTPStatus.NOT_FOUND
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    """Exception raised for status 409 (Conflict)."""

    def __init__(self, message="Conflict"):
        self.status_code = HTTPStatus.CONFLICT
        self.message = message
        super().__init__(self.message)


class InternalServerError(Exception):
    """Exception raised for status 500 (Internal Server Error)."""

    def __init__(self, message="Something went wrong"):
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = message
        super().__init__(self.message)


class GenerateError(Exception):
    """Generic error generation."""

    def __init__(self, error, status_code):
        self.message = error
        self.status_code = status_code
        super().__init__(self)


@exception_handler_bp.app_errorhandler(GenerateError)
def generate_exception(e):
    """Handles GenericError"""
    logger.exception(e)
    response = jsonify({"status": e.status_code, "msg": e.error})
    response.status_code = e.status_code

    return response


@exception_handler_bp.app_errorhandler(sqlalchemy.exc.InternalError)
def sql_error(e):
    """Handles internal sqlalchemy errors"""
    logger.exception(e)
    response = jsonify(
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "msg": f"SQL Error: {e.orig.args[1]}",
        }
    )
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    response.message = response["msg"]

    return response



@jwt.invalid_token_loader
def _expired_token_callbacks(c):  # pylint: disable=unused-argument
    """Handles JWT untreated invalid token errors"""
    return make_response(
        jsonify(
            {
                "status": 422,
                "msg": "Unidentified Token",
            }
        ),
        422,
    )


@jwt.unauthorized_loader
def _expired_token_callback(c):  # pylint: disable=unused-argument
    """Handles JWT untreated Unauthorized errors"""
    return make_response(
        jsonify(
            {
                "status": 401,
                "msg": "Token not sent",
            }
        ),
        401,
    )
