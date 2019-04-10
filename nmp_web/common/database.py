# coding: utf-8

from flask import current_app
from pymongo import MongoClient
import redis
import leancloud


redis_host = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['ip']
redis_port = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['port']
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

mongodb_client = MongoClient(current_app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['ip'],
                             current_app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['port'])

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status


# leancloud
leancloud_config = current_app.config['NWPC_MONITOR_WEB_CONFIG']['leancloud']
leancloud.init(leancloud_config["app_id"], leancloud_config["app_key"])


class Blob(leancloud.Object):
    pass
