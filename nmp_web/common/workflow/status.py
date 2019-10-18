# coding: utf-8
import datetime

from flask import current_app, json

from nmp_web.common.database import redis_client
from nmp_web.common.data_store.redis import save_workflow_status_blob


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
    current_app.logger.info("[{owner}/{repo}] save status to redis: {time}".format(
        owner=owner,
        repo=repo,
        time=redis_value['time'],
    ))
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    redis_client.set(key, json.dumps(redis_value))


def handle_nmp_model_message(owner, repo, message):
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
    save_workflow_status_blob(owner, repo, status_blob)

    # save to leancloud
    from nmp_web.common.data_store.leancloud import save_blob

    if aborted_blob:
        current_app.logger.info('[{owner}/{repo}] save aborted blob to leancloud...'.format(
            owner=owner, repo=repo
        ))
        save_blob(aborted_blob)
    else:
        current_app.logger.warn('[{owner}/{repo}] we don\'t save other blobs to leancloud'.format(
            owner=owner, repo=repo
        ))


def get_owner_repo_status_from_cache(owner, repo):
    from nmp_web.common.data_store.redis import get_workflow_status
    redis_value = get_workflow_status(owner, repo)
    if redis_value is None:
        # from nmp_web.common.data_store.leancloud import get_workflow_status
        # status = get_workflow_status(owner, repo)
        # if status is None:
        #     return None
        return None

        # redis_value = save_workflow_status_blob(owner, repo, status)
    return redis_value
