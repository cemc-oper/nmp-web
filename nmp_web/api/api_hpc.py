import gzip

from flask import request, json, jsonify, url_for, current_app

from nmp_web.common.database import mongodb_client
from nmp_web.api import api_app
from nmp_web.common import analytics
from nmp_web.common import data_store

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status


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
    data_store.save_disk_usage_to_mongodb(user, value)

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
    result = data_store.get_disk_usage_from_mongodb(user)
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
    data_store.save_disk_space_to_mongodb(value)

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
    result = data_store.get_disk_space_from_mongodb()
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/status', methods=['POST'])
def receive_loadleveler_status(user):
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

    if message['data']['type'] == 'takler_object':
        abnormal_jobs_blob = None
        for a_blob in message['data']['blobs']:
            if (
                a_blob['data']['type'] == 'hpc_loadleveler_status' and
                a_blob['data']['name'] == 'abnormal_jobs'
            ):
                abnormal_jobs_blob = a_blob

        if abnormal_jobs_blob is None:
            result = {
                'status': 'error',
                'message': 'can\'t find a abnormal jobs blob.'
            }
            return jsonify(result)

        tree_object = message['data']['trees'][0]
        commit_object = message['data']['commits'][0]

        # 保存到 mongodb
        blobs_collection = nwpc_monitor_platform_mongodb.blobs
        blobs_collection.insert_one(abnormal_jobs_blob)

        trees_collection = nwpc_monitor_platform_mongodb.trees
        trees_collection.insert_one(tree_object)

        commits_collection = nwpc_monitor_platform_mongodb.commits
        commits_collection.insert_one(commit_object)
    elif message['data']['type'] == 'nmp_model':
        # TODO: nmp_model
        current_app.logger.warn("message type is not supported: nmp_model".format())
    elif message['data']['type'] == 'nmp_model_job_list':
        # TODO: nmp_model
        current_app.logger.warn("message type is not supported: nmp_model_job_list".format())
    elif message['data']['type'] == 'job_list':
        value = message
        data_store.save_hpc_loadleveler_status_to_cache(user, value)

    # send data to google analytics
    analytics.send_google_analytics_page_view(
        url_for('api_app.receive_loadleveler_status', user=user)
    )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/status', methods=['GET'])
def request_loadleveler_status(user):
    result = data_store.get_hpc_loadleveler_status_from_cache(user)
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/abnormal_jobs/<int:abnormal_jobs_id>', methods=['GET'])
def get_hpc_loadleveler_status_abnormal_jobs(user, abnormal_jobs_id):
    abnormal_jobs_content = {
        'update_time': None,
        'plugin_name': None,
        'abnormal_job_list': [],
        'abnormal_jobs_id': abnormal_jobs_id
    }

    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    query_key = {
        'owner': user,
        'repo': 'hpc',
        'id': abnormal_jobs_id
    }
    query_result = blobs_collection.find_one(query_key)
    if not query_result:
        return jsonify(abnormal_jobs_content)

    blob_content = query_result['data']['content']

    abnormal_jobs_content['update_time'] = blob_content['update_time']
    abnormal_jobs_content['plugin_name'] = blob_content['update_time']
    abnormal_jobs_content['abnormal_job_list'] = blob_content['abnormal_job_list']
    abnormal_jobs_content['abnormal_jobs_id'] = abnormal_jobs_id

    return jsonify(abnormal_jobs_content)
