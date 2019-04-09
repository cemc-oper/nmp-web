# coding: utf-8
import gzip

from flask import request, json, jsonify

from nmp_web.api import api_app
from nmp_web.api.api_workflow import nwpc_monitor_platform_mongodb
from nmp_web.common.operation_system import owner_list


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

    if message['data']['type'] == 'takler_object':
        unfit_nodes_blob = None
        for a_blob in message['data']['blobs']:
            if a_blob['data']['type'] == 'unfit_nodes':
                unfit_nodes_blob = a_blob

        if unfit_nodes_blob is None:
            result = {
                'status': 'error',
                'message': 'can\'t find a unfit nodes blob.'
            }
            return jsonify(result)

        tree_object = message['data']['trees'][0]
        commit_object = message['data']['commits'][0]

        # 保存到 mongodb
        blobs_collection = nwpc_monitor_platform_mongodb.blobs
        blobs_collection.insert_one(unfit_nodes_blob)

        trees_collection = nwpc_monitor_platform_mongodb.trees
        trees_collection.insert_one(tree_object)

        commits_collection = nwpc_monitor_platform_mongodb.commits
        commits_collection.insert_one(commit_object)
    elif message['data']['type'] == 'nmp_model':
        unfit_nodes_blob = None
        for a_blob in message['data']['blobs']:
            if a_blob['_cls'] == 'Blob.UnfitNodesBlob':
                unfit_nodes_blob = a_blob

        if unfit_nodes_blob is None:
            result = {
                'status': 'error',
                'message': 'can\'t find a unfit nodes blob.'
            }
            return jsonify(result)

        tree_object = message['data']['trees'][0]
        commit_object = message['data']['commits'][0]

        # 保存到 mongodb
        blobs_collection = nwpc_monitor_platform_mongodb.blobs
        blobs_collection.insert_one(unfit_nodes_blob)

        trees_collection = nwpc_monitor_platform_mongodb.trees
        trees_collection.insert_one(tree_object)

        commits_collection = nwpc_monitor_platform_mongodb.commits
        commits_collection.insert_one(commit_object)
    else:
        raise ValueError('data type is not supported: {data_type}'.format(data_type=message['data']['type']))

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

    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    query_key = {
        'owner': owner,
        'repo': repo,
        'ticket_id': unfit_nodes_id
    }
    query_result = blobs_collection.find_one(query_key)
    if not query_result:
        return jsonify(unfit_nodes_content)

    blob_content = query_result['data']['content']

    unfit_nodes_content = blob_content

    return jsonify(unfit_nodes_content)