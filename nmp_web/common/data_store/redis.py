# coding: utf-8
from flask import json

from nmp_web.common.database import redis_client, nwpc_monitor_platform_mongodb

weixin_access_token_key = "weixin_access_token"


def get_weixin_access_token_from_cache() -> str or None:
    weixin_access_token = redis_client.get(weixin_access_token_key)
    if weixin_access_token is None:
        return None
    weixin_access_token = weixin_access_token.decode()
    return weixin_access_token


def save_weixin_access_token_to_cache(access_token: str) -> None:
    redis_client.set(weixin_access_token_key, access_token)
    return


# workflow
def get_owner_repo_status_from_cache(owner, repo):
    key = "{owner}/{repo}/status".format(owner=owner, repo=repo)
    message_string = redis_client.get(key)
    if message_string is None:
        mongodb_key = {
            'owner': owner,
            'repo': repo
        }
        record = nwpc_monitor_platform_mongodb.sms_server_status.find_one(
            mongodb_key, {"_id": 0}
        )
        if record is None:
            return None

        redis_value = {
            'owner': owner,
            'repo': repo,
            'sms_name': repo,
            'time': record['collected_time'],
            'status': record['status'],
            'type': 'sms'
        }

        redis_client.set(key, json.dumps(redis_value))
        return record
    else:
        message_string = message_string.decode()
    return json.loads(message_string)