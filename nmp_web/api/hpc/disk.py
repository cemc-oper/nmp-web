# coding: utf-8
import gzip

from flask import request, json, jsonify, url_for

import nmp_web.common.data_store.mongodb
from nmp_web.api import api_app
from nmp_web.common import data_store, analytics


@api_app.route('/hpc/users/<user>/disk/usage', methods=['POST'])
def receive_disk_usage(user):
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    nmp_web.common.data_store.mongodb.save_disk_usage_to_mongodb(user, value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_disk_usage', user=user)
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/disk/usage', methods=['GET'])
def request_disk_usage(user):
    result = nmp_web.common.data_store.mongodb.get_disk_usage_from_mongodb(user)
    return jsonify(result)


@api_app.route('/hpc/info/disk/space', methods=['POST'])
def receive_disk_space():
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    value = message
    nmp_web.common.data_store.mongodb.save_disk_space_to_mongodb(value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_disk_space')
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/info/disk/space', methods=['GET'])
def request_disk_space():
    result = nmp_web.common.data_store.mongodb.get_disk_space_from_mongodb()
    return jsonify(result)
