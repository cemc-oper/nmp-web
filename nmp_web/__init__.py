# coding=utf-8
from pathlib import Path
import logging

from flask import Flask

from nmp_web.util.converter import NoStaticConverter
from nmp_web.util.json_encoder import NwpcMonitorWebApiJSONEncoder
from nmp_web.common.config import load_config


def create_app(config_file_path=None):
    static_folder = str(Path(Path(__file__).parent.parent, "static"))
    template_folder = str(Path(Path(__file__).parent.parent, "templates"))
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.config.from_object(load_config(config_file_path))

    app.json_encoder = NwpcMonitorWebApiJSONEncoder
    app.url_map.converters['no_static'] = NoStaticConverter

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)

    with app.app_context():
        import nmp_web.common.database
        import nmp_web.controller

        from nmp_web.api import api_app
        app.register_blueprint(api_app, url_prefix="/api/v1")

    return app
