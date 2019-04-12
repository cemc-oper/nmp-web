# coding: utf-8
import datetime

import leancloud


class Blob(leancloud.Object):
    pass


class HpcDiskUsage(leancloud.Object):
    pass


class HpcDiskSpace(leancloud.Object):
    pass


class HpcLoadLeveler(leancloud.Object):
    pass


class WorkflowStatus(leancloud.Object):
    pass


def save_blob(blob: dict) -> None:
    b = Blob()
    blob['timestamp'] = datetime.datetime.strptime(blob['timestamp'], "%Y-%m-%dT%H:%M:%S")
    b.set(blob)
    b.save()


def get_blob(ticket_id: int) -> Blob or None:
    query = leancloud.Query(Blob)
    query.equal_to('ticket_id', ticket_id)
    query_list = query.find()
    if len(query_list) == 0:
        return None
    return query_list[0]


def _save_workflow_status(owner, repo, blob) -> None:
    # WARNING: don't use this because LeanCloud AVObject can only store object smaller than 128KB.
    #   Maybe AVFile should be used together with AVObject.
    b = WorkflowStatus()
    blob['timestamp'] = datetime.datetime.strptime(blob['timestamp'], "%Y-%m-%dT%H:%M:%S")
    b.set(blob)
    b.set('owner', owner)
    b.set('repo', repo)
    b.save()


def get_workflow_status(owner, repo) -> WorkflowStatus or None:
    query1 = WorkflowStatus.query
    query2 = WorkflowStatus.query

    query1.equal_to('owner', owner)
    query2.equal_to('repo', repo)

    query = leancloud.Query.and_(query1, query2)

    query_list = query.find()
    if len(query_list) == 0:
        return None
    return query_list[0]


def save_disk_usage(user: str, value: dict) -> None:
    b = get_disk_usage(user)
    if b is None:
        b = HpcDiskUsage()
        b.set('user', user)
    b.set(value)
    b.save()


def get_disk_usage(user: str) -> HpcDiskUsage or None:
    query = leancloud.Query(HpcDiskUsage)
    query.equal_to('user', user)
    query_list = query.find()
    if len(query_list) == 0:
        return None
    return query_list[0]


def save_disk_space(value: dict) -> None:
    b = get_disk_space()
    if b is None:
        b = HpcDiskSpace()
    b.set(value)
    b.save()


def get_disk_space() -> HpcDiskSpace or None:
    query = leancloud.Query(HpcDiskSpace)
    query_list = query.find()
    if len(query_list) == 0:
        return None
    return query_list[0]


def save_hpc_loadleveler(user: str, value: dict) -> None:
    b = get_hpc_loadleveler(user)
    if b is None:
        b = HpcLoadLeveler()
        b.set('user', user)
    b.set(value)
    b.save()


def get_hpc_loadleveler(user: str) -> HpcLoadLeveler or None:
    query = leancloud.Query(HpcLoadLeveler)
    query.equal_to('user', user)
    query_list = query.find()
    if len(query_list) == 0:
        return None
    return query_list[0]
