# coding=utf-8
import redis
from flask import Flask
from pymongo import MongoClient

from nmp_web.util.converter import NoStaticConverter
from nmp_web.util.json_encoder import NwpcMonitorWebApiJSONEncoder
from nmp_web.app_config import load_config

app = Flask(__name__, static_url_path='/static', static_folder='../static')

app.config.from_object(load_config())
redis_host = app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['ip']
redis_port = app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['port']
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

mongodb_client = MongoClient(app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['ip'],
                             app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['port'])

app.json_encoder = NwpcMonitorWebApiJSONEncoder
app.url_map.converters['no_static'] = NoStaticConverter

app.secret_key = '\x99g\x0b\xedY\xcf\n\xdd\xeb\xd7\\2K\xf94Cq{\xea\xe6\x8c\x17\xdf\x10'

from nmp_web.api import api_app
app.register_blueprint(api_app, url_prefix="/api/v1")

