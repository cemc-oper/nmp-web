# coding: utf-8
import gzip

from flask import request, json, jsonify, current_app, url_for

from nmp_web.common.data_store.leancloud import get_hpc_loadleveler, get_blob
from nmp_web.api import api_app
# from nmp_web.common import analytics


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

    from nmp_web.common.workload.loadleveler import handle_message
    handle_message(user, "loadleveler", message)

    # send data to google analytics
    # analytics.send_google_analytics_page_view(
    #     url_for('api_app.receive_loadleveler_status', user=user)
    # )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/status', methods=['GET'])
def request_loadleveler_status(user):
    result = get_hpc_loadleveler(user)
    return jsonify(result)


@api_app.route('/hpc/users/<user>/loadleveler/abnormal_jobs/<int:abnormal_jobs_id>', methods=['GET'])
def get_hpc_loadleveler_status_abnormal_jobs(user, abnormal_jobs_id):
    abnormal_jobs_content = {
        'update_time': None,
        'plugins': None,
        'abnormal_jobs': [],
        'abnormal_jobs_id': abnormal_jobs_id
    }

    query_result = get_blob(abnormal_jobs_id)
    if not query_result:
        return jsonify(abnormal_jobs_content)

    blob_data = query_result['data']
    blob_content = blob_data['content']

    abnormal_jobs_content['update_time'] = blob_data['update_time']
    abnormal_jobs_content['plugins'] = blob_content['plugins']
    abnormal_jobs_content['abnormal_jobs'] = blob_content['abnormal_jobs']
    abnormal_jobs_content['abnormal_jobs_id'] = abnormal_jobs_id

    return jsonify(abnormal_jobs_content)