from flask import json
from nmp_web import redis_client, mongodb_client

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

owner_list = {
    'nwp_xp': {
        'repos': [
            {'id': 1, 'name': 'nwpc_op'},
            {'id': 2, 'name': 'nwpc_qu'},
            {'id': 3, 'name': 'eps_nwpc_qu'},
            {'id': 4, 'name': 'nwpc_pd'},
            {'id': 5, 'name': 'draw_ncl'},
            {'id': 6, 'name': 'pi_nwpc_op'},
            {'id': 7, 'name': 'pi_nwpc_qu'},
            {'id': 8, 'name': 'pi_eps_nwpc_qu'},
            {'id': 9, 'name': 'pi_nwpc_pd'},
        ]
    },
    'nwp_pos': {
        'repos': [
            {'id': 1, 'name': 'nwpc_sp'},
        ]
    },
    'nwp_vfy': {
        'repos': [
            {'id': 1, 'name': 'nwpc_nwp_vfy'}
        ]
    },
    'wangdp': {
        'repos': [
            {'id': 1, 'name': 'nwpc_wangdp'}
        ]
    }
}


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