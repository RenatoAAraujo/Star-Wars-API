"""Flask app creatrion with flask-restx"""
import logging
import os

from flask import Flask
from flask_restx import Api
from waitress import serve

from app.services.extensions import cache, jwt, ma
from database.config_sqlalchemy import db, migrate


def create_app(_api, deploy_env="Testing"):
    """create and configure the flask application"""
    # app
    _app = Flask(__name__)
    if not deploy_env:
        raise ValueError("Invalid APP_ENV!")
    _app.config.from_object(f"config.{os.environ.get('APP_ENV')}Config")

    try:
        os.makedirs(_app.instance_path, exist_ok=True)
    except OSError as _e:
        print(f'Error in "app.instance_path"\nError: {str(_e)}')

    # extentions
    resgister_extentions(_app)

    # logger
    logger_lv = (
        logging.WARN
        if os.environ.get("APP_ENV", "development") == "production"
        else logging.DEBUG
    )
    logging.basicConfig(
        level=logger_lv,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s",
    )

    # API
    _api.init_app(_app)

    return _app


def resgister_extentions(_app):
    # jwt
    jwt.init_app(_app)
    jwt.init_app(_app)

    # database
    db.init_app(_app)
    migrate.init_app(_app, db, compare_type=True)
    ma.init_app(_app)
    cache.init_app(_app)


def register_namespaces():
    """Register all flask-restx namespace to the API"""
    # admin
    from app.admin.group.views import group_api

    api.add_namespace(group_api, path="/api/v1/admin/groups")

    from app.admin.health.views import health_api

    api.add_namespace(health_api, path="/api/v1/admin/health")

    from app.admin.users.views import user_admin_api

    api.add_namespace(user_admin_api, path="/api/v1/admin/users")

    # auth
    from app.auth.views import auth_api

    api.add_namespace(auth_api, path="/api/v1/auth")

    # star wars
    from app.star_wars.views import star_wars_api

    api.add_namespace(star_wars_api, path="/")


def register_models():
    from app.services.sqlalchemy.swagger.models import (
        null_pagination_info,
        pagination_info,
    )

    api.models["null_pagination_info"] = null_pagination_info
    api.models["pagination_info"] = pagination_info

    from app.services.exceptions.swagger.models import error_data_model, error_model

    api.models["error_data"] = error_data_model
    api.models["error"] = error_model


api = Api(
    version="1.0",
    title="Star Wars API",
    description="An integration with the Star Wars API",
    doc="/doc",
)
register_namespaces()
register_models()


app = create_app(api, deploy_env=os.environ.get("APP_ENV"))
port = os.environ.get("PORT", "5000")


if os.environ.get("APP_ENV", "development") == "production":
    app.logger.info(
        "Environment prod running. Port %s", port
    )  # pylint: disable=no-member
    serve(app, host="0.0.0.0", port=port)
else:
    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except (Exception,) as e:
        print(f"Error:\n{str(e)}")
