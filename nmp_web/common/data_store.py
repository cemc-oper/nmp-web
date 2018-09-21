from nmp_web import mongodb_client

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status
hpc_disk_usage_status = nwpc_monitor_platform_mongodb.hpc_disk_usage_status
hpc_disk_space_status = nwpc_monitor_platform_mongodb.hpc_disk_space_status
hpc_loadleveler_status = nwpc_monitor_platform_mongodb.hpc_loadleveler_status


# disk usage


def save_disk_usage_to_mongodb(user: str, value: dict) -> None:
    key = {
        "user": user
    }
    hpc_disk_usage_status.update(key, value, upsert=True)


def get_disk_usage_from_mongodb(user: str) -> dict:
    key = {
        'user': user
    }
    result = hpc_disk_usage_status.find_one(key, {"_id": 0})
    return result


def save_disk_space_to_mongodb(value: dict) -> None:
    key = {
        "user": 'hpc'
    }
    hpc_disk_space_status.update(key, value, upsert=True)


def get_disk_space_from_mongodb() -> dict:
    key = {
        'user': 'hpc'
    }
    result = hpc_disk_space_status.find_one(key, {"_id": 0})
    return result


# loadleveler status


def save_hpc_loadleveler_status_to_cache(user: str, value: dict) -> tuple:
    key = {
        'data.user': user
    }
    hpc_loadleveler_status.update(key, value, upsert=True)
    return key, value


def get_hpc_loadleveler_status_from_cache(user: str) -> dict:
    key = {
        'data.user': user
    }
    value = hpc_loadleveler_status.find_one(key, {"_id": 0})
    return value
