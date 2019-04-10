# coding: utf-8


def test_status(app):
    from nmp_web.common.workflow.status import handle_status_message
    with app.app_context():
        message_dict = {
            'app': 'nmp_broker',
            'data': {
                'type': 'status',
                'server_name': 'nwpc_op',
                'time': '2018-09-21T15:20:59.667581',
                'status': {
                    "name": "",
                    "node_type": "root",
                    "node_path": "/",
                    "path": "/",
                    "status": "complete",
                    "children": [
                        {
                            "name": "windroc_test_suite",
                            "children": [
                                {
                                    "name": "initial",
                                    "children": [],
                                    "node_type": "task",
                                    "node_path": "/windroc_test_suite/initial",
                                    "path": "/windroc_test_suite/initial",
                                    "status": "complete"
                                }
                            ],
                            "node_type": "suite",
                            "node_path": "/windroc_test_suite",
                            "path": "/windroc_test_suite",
                            "status": "complete"
                        },
                        {
                            "name": "grapes_meso_3km_post",
                            "node_type": "suite",
                            "node_path": "/grapes_meso_3km_post",
                            "path": "/grapes_meso_3km_post",
                            "status": "complete",
                            "children": [
                                {
                                    "name": "00",
                                    "node_type": "family",
                                    "node_path": "/grapes_meso_3km_post/00",
                                    "path": "/grapes_meso_3km_post/00",
                                    "status": "complete",
                                    "children": [
                                        {
                                            "name": "initial",
                                            "children": [],
                                            "node_type": "task",
                                            "node_path": "/grapes_meso_3km_post/00/initial",
                                            "path": "/grapes_meso_3km_post/00/initial",
                                            "status": "complete"
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            'event': 'post_ecflow_status',
            'timestamp': '2019-04-09T08:04:57'
        }
    handle_status_message('nwp_xp', 'nwpc_op', message_dict)


if __name__ == "__main__":
    from nmp_web import create_app
    app = create_app()
    test_status(app)
