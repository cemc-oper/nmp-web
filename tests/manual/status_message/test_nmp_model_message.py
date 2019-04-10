# coding: utf-8


def test_nmp_model(app):
    from nmp_web.common.workflow import handle_nmp_model_message
    with app.app_context():
        message_dict = {
            'app': 'nmp_broker',
            'data': {
                'blobs': [
                    {
                        '_cls': 'Blob.StatusBlob',
                        '_id': '5cac5228e202216d6d33bef7',
                        'data': {
                            '_cls': 'StatusBlobData',
                            'content': {
                                'collected_time': '2018-09-21T15:20:59',
                                'server_name': 'nwpc_op',
                                'status': {
                                    'children': [
                                        {
                                            'children':
                                                [
                                                    {
                                                        'children': [], 'name': 'initial',
                                                        'node_path': '/windroc_test_suite/initial',
                                                        'node_type': 'task',
                                                        'path': '/windroc_test_suite/initial',
                                                        'status': 'complete'
                                                    }
                                                ],
                                            'name': 'windroc_test_suite',
                                            'node_path': '/windroc_test_suite',
                                            'node_type': 'suite',
                                            'path': '/windroc_test_suite',
                                            'status': 'complete'
                                        },
                                        {
                                            'children': [
                                                {
                                                    'children': [
                                                        {
                                                            'children': [],
                                                            'name': 'initial',
                                                            'node_path': '/grapes_meso_3km_post/00/initial',
                                                            'node_type': 'task',
                                                            'path': '/grapes_meso_3km_post/00/initial',
                                                            'status': 'aborted'
                                                        }
                                                    ],
                                                    'name': '00',
                                                    'node_path': '/grapes_meso_3km_post/00',
                                                    'node_type': 'family',
                                                    'path': '/grapes_meso_3km_post/00',
                                                    'status': 'aborted'
                                                }
                                            ],
                                            'name': 'grapes_meso_3km_post',
                                            'node_path': '/grapes_meso_3km_post',
                                            'node_type': 'suite',
                                            'path': '/grapes_meso_3km_post',
                                            'status': 'aborted'
                                        }
                                    ],
                                    'name': '',
                                    'node_path': '/',
                                    'node_type': 'root',
                                    'path': '/',
                                    'status': 'aborted'
                                },
                                'update_time': '2019-04-09T08:04:56'
                            },
                            'name': 'server_status',
                            'type': 'StatusBlobData'
                        },
                        'owner': 'nwp_xp',
                        'repo': 'nwpc_op',
                        'ticket_id': 29321,
                        'timestamp': '2019-04-09T08:04:56'
                    },
                    {
                        '_cls': 'Blob.AbortedTasksBlob',
                        '_id': '5cac5228e202216d6d33bef8',
                        'data': {
                            '_cls': 'AbortedTasksBlobData',
                            'content': {
                                'collected_time': '2018-09-21T15:20:59',
                                'server_name': 'server_aborted_tasks',
                                'status_blob_ticket_id': 29321,
                                'tasks': [
                                    {
                                        'children': [],
                                        'name': 'initial',
                                        'node_type': 'task',
                                        'path': '/grapes_meso_3km_post/00/initial',
                                        'status': 'aborted'
                                    }
                                ]
                            },
                            'name': 'server_aborted_tasks'
                        },
                        'owner': 'nwp_xp',
                        'repo': 'nwpc_op',
                        'ticket_id': 29322,
                        'timestamp': '2019-04-09T08:04:56'
                    }
                ],
                'commits': [
                    {
                        '_cls': 'WorkflowCommit',
                        '_id': '5cac5228e202216d6d33befa',
                        'data': {
                            '_cls': 'WorkflowCommitData',
                            'committed_time': '2019-04-09T08:04:56',
                            'committer': 'aix',
                            'tree_ticket_id': 29323,
                            'type': 'status'
                        },
                        'owner': 'nwp_xp',
                        'repo': 'nwpc_op',
                        'ticket_id': 29324,
                        'timestamp': '2019-04-09T08:04:56'
                    }
                ],
                'trees': [
                    {
                        '_cls': 'Tree',
                        '_id': '5cac5228e202216d6d33bef9',
                        'owner': 'nwp_xp',
                        'repo': 'nwpc_op',
                        'ticket_id': 29323,
                        'timestamp': '2019-04-09T08:04:56'
                    }
                ],
                'type': 'nmp_model'
            },
            'event': 'post_ecflow_status',
            'timestamp': '2019-04-09T08:04:57'
        }

        handle_nmp_model_message('nwpc_xp', 'nwpc_op', message_dict)


if __name__ == "__main__":
    from nmp_web import create_app
    app = create_app()
    test_nmp_model(app)
