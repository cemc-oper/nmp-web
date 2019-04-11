# coding: utf-8
from flask import json

from nmp_web.common.database import redis_client


weixin_access_token_key = "weixin_access_token"


def save_workflow_status_blob(owner, repo, status_blob):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    redis_value = {
        'owner': owner,
        'repo': repo,
        'sms_name': repo,
        'time': status_blob['data']['content']['collected_time'],
        'status': status_blob['data']['content']['status'],
        'type': 'sms'
    }
    redis_client.set(key, json.dumps(redis_value))
    return redis_value


def get_workflow_status(owner, repo):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    message_string = redis_client.get(key)
    if message_string is None:
        return None
    else:
        return json.loads(message_string)


def get_weixin_access_token_from_cache() -> str or None:
    weixin_access_token = redis_client.get(weixin_access_token_key)
    if weixin_access_token is None:
        return None
    weixin_access_token = weixin_access_token.decode()
    return weixin_access_token


def save_weixin_access_token_to_cache(access_token: str) -> None:
    redis_client.set(weixin_access_token_key, access_token)
    return
