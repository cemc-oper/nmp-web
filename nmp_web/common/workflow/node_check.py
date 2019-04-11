# coding: utf-8
import warnings

from flask import jsonify
from nmp_web.common.database import nwpc_monitor_platform_mongodb


def handle_node_check_message(owner, repo, message):
    data_type = message['data']['type']
    handler_mapper = {
        'nmp_model': _handle_nmp_model_message,
        'takler_object': _handle_takler_message,
    }
    if data_type in handler_mapper:
        handler_mapper[data_type](owner, repo, message)
    else:
        raise ValueError('data type is not supported: {data_type}'.format(data_type=message['data']['type']))


def _handle_nmp_model_message(owner, repo, message):
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


def _handle_takler_message(owner, repo, message):
    warnings.warn("takler is deprecated, please use nmp_model", DeprecationWarning)
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
