# coding: utf-8
import datetime
import gzip

from flask import request, json, jsonify, current_app

from nmp_web.api import api_app
from nmp_web.common.workflow import owner_list
from nmp_web.common.workflow.status import get_owner_repo_status_from_cache

try:
    a = datetime.datetime.fromisoformat
except AttributeError:
    from backports.datetime_fromisoformat import MonkeyPatch
    MonkeyPatch.patch_fromisoformat()


@api_app.route('/workflow/owners/<owner>/repos', methods=['GET'])
def get_owner_repos(owner: str):
    # get repo list
    repo_list = []
    if owner in owner_list:
        repo_list = owner_list[owner]['repos']

    # get status for each repo in repo list
    owner_repo_status = []
    for a_repo in repo_list:
        a_repo_name = a_repo['name']
        cache_value = get_owner_repo_status_from_cache(owner, a_repo_name)
        repo_status = None
        last_updated_time = None
        if cache_value is not None:
            bunch_dict = cache_value['status']

            repo_status = bunch_dict['status']
            time_string = cache_value['time']
            data_collect_datetime = datetime.datetime.fromisoformat(time_string)
            last_updated_time = data_collect_datetime.strftime('%Y-%m-%d %H:%M:%S')
        owner_repo_status.append({
            'owner': owner,
            'repo': a_repo_name,
            'status': repo_status,
            'last_updated_time': last_updated_time
        })

    return jsonify(owner_repo_status)


@api_app.route('/repos/<owner>/<repo>/sms/status', methods=['POST'])
@api_app.route('/workflow/repos/<owner>/<repo>/status/head', methods=['POST'])
def post_workflow_status(owner, repo):
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])
    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    from nmp_web.common.workflow.status import handle_message
    handle_message(owner, repo, message)

    # send data to google analytics
    # NOTE: close google analytics
    # analytics.send_google_analytics_page_view(
    #     url_for('api_app.post_workflow_status', owner=owner, repo=repo)
    # )

    result = {
        'status': 'ok'
    }
    return jsonify(result)


@api_app.route('/workflow/repos/<owner>/<repo>/status/head/', methods=['GET'])
@api_app.route('/workflow/repos/<owner>/<repo>/status/head/<path:sms_path>', methods=['GET'])
def get_repo_status(owner: str, repo: str, sms_path: str = '/'):
    path = '/'
    last_updated_time = None
    children_status = []

    node_status = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    result = {
        'app': 'nmp_web',
        'type': 'repo',
        'data': {
            'node_status': node_status
        }
    }

    current_app.logger.info("get repo status")

    if owner not in owner_list:
        return jsonify(result)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return jsonify(result)

    cache_value = get_owner_repo_status_from_cache(owner, repo)
    node_status = None
    if cache_value is not None:
        time_string = cache_value['time']
        data_collect_datetime = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
        last_updated_time = data_collect_datetime.strftime('%Y-%m-%d %H:%M:%S')

        bunch_dict = cache_value['status']

        def find_node(root, a_path):
            if a_path == '' or a_path == '/':
                return root, None
            tokens = a_path.split("/")
            cur_node = root
            parent_node = None
            for a_token in tokens:
                t_node = None
                for a_child_node in cur_node['children']:
                    if a_child_node['name'] == a_token:
                        t_node = a_child_node
                        break
                if t_node is None:
                    return None
                parent_node = cur_node
                cur_node = t_node
            return cur_node, parent_node
        node, p_node = find_node(bunch_dict, sms_path)
        if node is not None:
            children_status = []
            if p_node:
                children_status.append(
                    {
                        'name': '..',
                        'path': p_node['path'],
                        'status': p_node['status'],
                        'has_children': True
                    }
                )
            path = node['path']
            for a_child in node['children']:
                if len(a_child['children']) > 0:
                    has_children = True
                else:
                    has_children = False
                children_status.append({
                    'name': a_child['name'],
                    'path': a_child['path'],
                    'status': a_child['status'],
                    'has_children': has_children
                })

    result['data']['node_status'] = {
        'owner': owner,
        'repo': repo,
        'path': path,
        'last_updated_time': last_updated_time,
        'children': children_status
    }

    return jsonify(result)


@api_app.route('/workflow/repos/<owner>/<repo>/aborted_tasks/<int:aborted_id>', methods=['GET'])
def get_repo_aborted_tasks(owner, repo, aborted_id):
    aborted_tasks_content = {
        'update_time': None,
        'collected_time': None,
        'status_blob_id': None,
        'tasks': []
    }

    if owner not in owner_list:
        return jsonify(aborted_tasks_content)

    found_repo = False
    for a_repo in owner_list[owner]['repos']:
        if repo == a_repo['name']:
            found_repo = True
            break
    if not found_repo:
        return jsonify(aborted_tasks_content)

    # blobs_collection = nwpc_monitor_platform_mongodb.blobs
    # query_key = {
    #     'owner': owner,
    #     'repo': repo,
    #     'ticket_id': aborted_id
    # }
    # query_result = blobs_collection.find_one(query_key)

    from nmp_web.common.data_store.leancloud import get_blob
    blob = get_blob(aborted_id)

    if blob is None:
        return jsonify(aborted_tasks_content)

    blob_content = blob.get('data')['content']

    aborted_tasks_content = {
        'update_time': blob.get('timestamp'),
        'collected_time': blob_content['collected_time'],
        'status_blob_id': blob_content['status_blob_ticket_id'],
        'tasks': blob_content['tasks']
    }

    return jsonify(aborted_tasks_content)
