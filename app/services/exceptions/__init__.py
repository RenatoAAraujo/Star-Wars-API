"""Exception_handler_blueprint"""
from flask import Blueprint

exception_handler_bp = Blueprint("exception_handler_bp", __name__)
from . import errors  # pylint: disable=wrong-import-position
