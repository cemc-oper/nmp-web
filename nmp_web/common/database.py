# coding: utf-8
from flask import current_app
import redis
import leancloud


redis_host = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['ip']
redis_port = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['port']
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)


# leancloud
leancloud_config = current_app.config['NWPC_MONITOR_WEB_CONFIG']['leancloud']
leancloud.init(leancloud_config["app_id"], leancloud_config["app_key"])
