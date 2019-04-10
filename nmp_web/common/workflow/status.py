# coding: utf-8
import datetime

from flask import current_app, json

from nmp_web.common.database import redis_client


def handle_message(owner, repo, message):
    data_type = message['data']['type']
    current_app.logger.info("[{owner}/{repo}]data type: {data_type}".format(
        owner=owner,
        repo=repo,
        data_type=data_type,
    ))

    mapper ={
        'status': handle_status_message,
        'nmp_model': handle_nmp_model_message,
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


def handle_nmp_model_message(owner, repo, message):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    status_blob = None
    aborted_blob = None
    for a_blob in message['data']['blobs']:
        if a_blob['_cls'] == 'Blob.StatusBlob':
            status_blob = a_blob
        if a_blob['_cls'] == 'Blob.AbortedTasksBlob':
            aborted_blob = a_blob

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

    # save to leancloud
    from nmp_web.common.database import Blob

    if aborted_blob:
        current_app.logger.info('[{owner}/{repo}] save aborted blob to leancloud...'.format(
            owner=owner, repo=repo
        ))
        blob = Blob()
        aborted_blob['timestamp'] = datetime.datetime.strptime(aborted_blob['timestamp'], "%Y-%m-%dT%H:%M:%S")
        blob.set(aborted_blob)
        blob.save()
    else:
        current_app.logger.warn('[{owner}/{repo}] we don\'t save other blobs to leancloud'.format(
            owner=owner, repo=repo
        ))
