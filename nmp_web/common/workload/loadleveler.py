# coding: utf-8
import warnings

from flask import jsonify
from nmp_web.common.data_store.leancloud import save_hpc_loadleveler, save_blob


def handle_message(owner, repo, message):
    data_type = message['data']['type']
    handler_mapper = {
        'nmp_model_job_list': _handle_nmp_model_job_list_message,
        'nmp_model': _handle_nmp_model_message,
        'job_list': _handle_job_list_message,
        'takler_object': _handle_takler_message,
    }

    if data_type in handle_message:
        handler_mapper[data_type](owner, repo, message)
    else:
        raise ValueError("data type is not supported: {data_type}".format(data_type=data_type))


def _handle_nmp_model_job_list_message(owner, repo, message):
    value = message
    save_hpc_loadleveler(owner, value)


def _handle_job_list_message(owner, repo, message):
    warnings.warn("job_list is deprecated, please use nmp_model_job_list", DeprecationWarning)
    value = message
    save_hpc_loadleveler(owner, value)


def _handle_nmp_model_message(owner, repo, message):
    abnormal_jobs_blob = None
    for a_blob in message['data']['blobs']:
        if a_blob['data']['_cls'] == 'AbnormalJobsBlobData':
            abnormal_jobs_blob = a_blob

    if abnormal_jobs_blob is None:
        result = {
            'status': 'error',
            'message': 'can\'t find a abnormal jobs blob.'
        }
        return jsonify(result)

    # tree_object = message['data']['trees'][0]
    # commit_object = message['data']['commits'][0]

    # 保存到 mongodb
    # blobs_collection = nwpc_monitor_platform_mongodb.blobs
    # blobs_collection.insert_one(abnormal_jobs_blob)

    save_blob(abnormal_jobs_blob)

    # trees_collection = nwpc_monitor_platform_mongodb.trees
    # trees_collection.insert_one(tree_object)
    #
    # commits_collection = nwpc_monitor_platform_mongodb.commits
    # commits_collection.insert_one(commit_object)


def _handle_takler_message(owner, repo, message):
    warnings.warn("takler_object is deprecated, please use nmp_model", DeprecationWarning)
    abnormal_jobs_blob = None
    for a_blob in message['data']['blobs']:
        if (
                a_blob['data']['type'] == 'hpc_loadleveler_status' and
                a_blob['data']['name'] == 'abnormal_jobs'
        ):
            abnormal_jobs_blob = a_blob

    if abnormal_jobs_blob is None:
        result = {
            'status': 'error',
            'message': 'can\'t find a abnormal jobs blob.'
        }
        return jsonify(result)

    save_blob(abnormal_jobs_blob)

