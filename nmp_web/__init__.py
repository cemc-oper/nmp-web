# coding=utf-8
from pathlib import Path

from flask import Flask

from .util.converter import NoStaticConverter
from .util.json_encoder import NwpcMonitorWebApiJSONEncoder
from .app_config import load_config


def create_app(config_file_path=None):
    static_folder = str(Path(Path(__file__).parent.parent, "static"))
    template_folder = str(Path(Path(__file__).parent.parent, "templates"))
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.config.from_object(load_config(config_file_path))
    app.secret_key = '\x99g\x0b\xedY\xcf\n\xdd\xeb\xd7\\2K\xf94Cq{\xea\xe6\x8c\x17\xdf\x10'

    app.json_encoder = NwpcMonitorWebApiJSONEncoder
    app.url_map.converters['no_static'] = NoStaticConverter

    with app.app_context():
        import nmp_web.common.database
        import nmp_web.controller

        from nmp_web.api import api_app
        app.register_blueprint(api_app, url_prefix="/api/v1")

    return app
