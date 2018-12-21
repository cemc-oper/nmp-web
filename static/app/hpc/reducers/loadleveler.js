import {
    REQUEST_HPC_USER_LOADLEVELER_STATUS,
    RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS,
    REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS,
    RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS
} from '../actions/loadleveler_status'

export function loadleveler_status_reducer(state={
    loadleveler_status: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        job_queue: {
            user: null,
            update_time: null,
            job_list: [],
        },
        abnormal_jobs: {
            update_time: null,
            abnormal_jobs_id: null,
            plugin: null,
            abnormal_jobs: []
        },
        show_option: {
            type: 'BRIEF'
        }
    }
}, action) {
    switch(action.type){
        case REQUEST_HPC_USER_LOADLEVELER_STATUS:
        case REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS:
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
        case RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS:
            let data = action.response.data;
            let message = data['data']['message'];
            let update_time = message['time'];
            let user = data['user'];
            let jobs = message['data']['response']['items'];
            let job_queue = {
                user: user,
                update_time: update_time,
                job_list: jobs,
            };

            return Object.assign({}, state, {
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                job_queue: job_queue,
            });
        case RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS:
            data = action.response.data;
            let abnormal_jobs = {
                update_time: data['update_time'],
                plugin: data['plugin'],
                abnormal_jobs_id: data['abnormal_jobs_id'],
                abnormal_jobs: data['abnormal_jobs']
            };

            // return Object.assign({}, state, {
            //     status: {
            //         is_fetching: false,
            //         last_updated: Date.now()
            //     },
            //     abnormal_jobs: abnormal_jobs
            // });
            return {
                ...state,
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                abnormal_jobs: abnormal_jobs
            };
        default:
            return state;
    }
}