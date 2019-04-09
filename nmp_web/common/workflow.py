# coding: utf-8
from flask import current_app, json, jsonify
import warnings

from nmp_web.common.database import redis_client, nwpc_monitor_platform_mongodb


def handle_message(owner, repo, message):
    data_type = message['data']['type']
    current_app.logger.info("[{owner}/{repo}]data type: {data_type}".format(
        owner=owner,
        repo=repo,
        data_type=data_type,
    ))

    mapper ={
        'status': handle_status_message,
        'takler_object': handle_takler_object_message,
        'nmp_model': handle_nmp_model_message
    }

    if data_type in mapper:
        mapper[data_type](owner, repo, message)
    else:
        current_app.logger.error("[{owner}/{repo}]data type is not supported: {data_type}".format(
            owner=owner,
            repo=repo,
            data_type=data_type
        ))


def handle_status_message(owner, repo, message):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    redis_value = message['data']

    redis_value['type'] = 'sms'

    # 保存到本地缓存
    # TODO: use a single schema for mongodb cache and redis item.
    """
    redis_value:
    {
        "name": "sms_status_message_data",
        "type": "record",
        "fields": [
            {"name": "owner", "type": "string"},
            {"name": "repo", "type": "string"},
            {"name": "sms_name", "type": "string"},
            {"name": "time", "type": "string"},
            {
                "name": "status",
                "doc": "bunch status dict",
                "type": { "type": "node" }
            }
        ]
    }
    """
    redis_client.set(key, json.dumps(redis_value))


def handle_takler_object_message(owner, repo, message):
    warnings.warn("takler_object is deprecated, use nmp_model instead", DeprecationWarning)
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    status_blob = None
    aborted_blob = None
    for a_blob in message['data']['blobs']:
        if a_blob['data']['type'] == 'status':
            status_blob = a_blob
        if a_blob['data']['type'] == 'aborted_tasks':
            aborted_blob = a_blob

    if status_blob is None:
        result = {
            'status': 'error',
            'message': 'can\'t find a status blob.'
        }
        return jsonify(result)

    tree_object = message['data']['trees'][0]
    commit_object = message['data']['commits'][0]

    # 保存到本地缓存
    redis_value = {
        'owner': owner,
        'repo': repo,
        'sms_name': repo,
        'time': status_blob['data']['content']['collected_time'],
        'status': status_blob['data']['content']['status'],
        'type': 'sms'
    }
    redis_client.set(key, json.dumps(redis_value))

    # 保存到 mongodb
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    blobs_collection.insert_one(status_blob)
    if aborted_blob:
        blobs_collection.insert_one(aborted_blob)

    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object)

    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object)


def handle_nmp_model_message(owner, repo, message):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    status_blob = None
    aborted_blob = None
    for a_blob in message['data']['blobs']:
        if a_blob['_cls'] == 'Blob.StatusBlob':
            status_blob = a_blob
        if a_blob['_cls'] == 'Blob.AbortedTasksBlob':
            aborted_blob = a_blob
    # if status_blob is None:
    #     result = {
    #         'status': 'error',
    #         'message': 'can\'t find a status blob.'
    #     }
    #     return jsonify(result)

    tree_object = message['data']['trees'][0]
    commit_object = message['data']['commits'][0]

    # save to redis
    current_app.logger.info('[{owner}/{repo}] save status to redis...'.format(
        owner=owner, repo=repo
    ))
    redis_value = {
        'owner': owner,
        'repo': repo,
        'sms_name': repo,
        'time': status_blob['data']['content']['collected_time'],
        'status': status_blob['data']['content']['status'],
        'type': 'sms'
    }
    redis_client.set(key, json.dumps(redis_value))

    # save to mongodb
    # NOTE: ignore status blob to speed up.
    current_app.logger.info('[{owner}/{repo}] save status blob to mongo...'.format(
        owner=owner, repo=repo
    ))
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    # blobs_collection.insert_one(status_blob)
    if aborted_blob:
        current_app.logger.info('[{owner}/{repo}] save aborted blob to mongo...'.format(
            owner=owner, repo=repo
        ))
        blobs_collection.insert_one(aborted_blob)

    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object)

    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object)