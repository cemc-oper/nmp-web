# coding: utf-8
import gzip

from flask import request, json, jsonify

from nmp_web.api import api_app
from nmp_web.common.workflow import owner_list


@api_app.route('/workflow/repos/<owner>/<repo>/task_check', methods=['POST'])
def post_sms_task_check(owner, repo):
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

    from nmp_web.common.workflow.node_check import handle_node_check_message
    handle_node_check_message(owner, repo, message)

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/workflow/repos/<owner>/<repo>/task_check/unfit_nodes/<int:unfit_nodes_id>', methods=['GET'])
def get_repo_unfit_nodes(owner, repo, unfit_nodes_id):
    unfit_nodes_content = {
        'update_time': None,
        'name': None,
        'trigger': None,
        'unfit_node_list': []
    }

    if owner not in owner_list:
        return jsonify(unfit_nodes_content)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return jsonify(unfit_nodes_content)

    from nmp_web.common.data_store.leancloud import get_blob
    blob = get_blob(unfit_nodes_id)

    if blob is None:
        return jsonify(unfit_nodes_content)

    blob_content = blob.get('data')['content']

    unfit_nodes_content = blob_content

    return jsonify(unfit_nodes_content)
