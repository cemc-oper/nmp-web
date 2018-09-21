import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_HPC_USER_LOADLEVELER_STATUS,
    RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS,
    REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS,
    RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS
} from '../actions/loadleveler_status'

import {
    REQUEST_ADD_HPC_USER_DISK_USAGE,
    ADD_HPC_USER_DISK_USAGE_SUCCESS,
    CLEAR_HPC_DISK_USAGE_USERS
} from '../actions/disk_usage'

import {
    REQUEST_HPC_DISK_SPACE,
    RECEIVE_HPC_DISK_SPACE_SUCCESS
} from '../actions/disk_space'

import {
    loadleveler_status_reducer
} from './loadleveler'

import {
    disk_usage_reducer
} from './disk_usage'

import {
    disk_space_reducer
} from './disk_space'


function hpc_reducer(state={
    disk_usage: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        users: []
    },
    disk_space: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        file_systems: [],
        time: null
    },
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
            plugin_name: null,
            job_list: []
        },
        show_option: {
            type: 'BRIEF'  // BRIEF, DETAIL
        }
    }
}, action) {
    switch (action.type) {
        case REQUEST_ADD_HPC_USER_DISK_USAGE:
        case ADD_HPC_USER_DISK_USAGE_SUCCESS:
        case CLEAR_HPC_DISK_USAGE_USERS:
            return Object.assign({}, state, {
                disk_usage: disk_usage_reducer(state.disk_usage, action)
            });
        case REQUEST_HPC_USER_LOADLEVELER_STATUS:
        case RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS:
        case REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS:
        case RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS:
            return Object.assign({}, state, {
                loadleveler_status: loadleveler_status_reducer(state.loadleveler_status, action)
            });
        case REQUEST_HPC_DISK_SPACE:
        case RECEIVE_HPC_DISK_SPACE_SUCCESS:
            return Object.assign({}, state, {
                disk_space: disk_space_reducer(state.disk_space, action)
            });
        default:
            return state;
    }
}

const hpcAppReducer = combineReducers({
    hpc: hpc_reducer,
    routing
});

export default hpcAppReducer;