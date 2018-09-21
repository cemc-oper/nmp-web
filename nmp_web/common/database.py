# coding: utf-8

from flask import current_app
from pymongo import MongoClient
import redis


redis_host = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['ip']
redis_port = current_app.config['NWPC_MONITOR_WEB_CONFIG']['redis']['host']['port']
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

mongodb_client = MongoClient(current_app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['ip'],
                             current_app.config['NWPC_MONITOR_WEB_CONFIG']['mongodb']['host']['port'])