export const REQUEST_HPC_USER_LOADLEVELER_STATUS = 'REQUEST_HPC_USER_LOADLEVELER_STATUS';

export function requestHpcUserLoadlevelerStatus(user){
    return {
        type: REQUEST_HPC_USER_LOADLEVELER_STATUS,
        user
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS = 'RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS';

export function receiveHpcUserLoadlevelerStatusSuccess(response){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE = 'RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE';

export function receiveHpcUserLoadlevelerStatusFailure(error){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE,
        error
    }
}

export function fetchHpcUserLoadlevelerStatus(user){
    return function (dispatch) {
        dispatch(requestHpcUserLoadlevelerStatus(user));

        return $.getJSON('/api/v1/hpc/users/' + user + '/loadleveler/status', {} ,function(data){
            dispatch(
                receiveHpcUserLoadlevelerStatusSuccess({
                    data: data
                })
            );
        });
    };
}



export const REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS = 'REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS';

export function requestHpcUserLoadlevelerAbnormalJobs(user, abnormal_jobs_id){
    return {
        type: REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS,
        user,
        abnormal_jobs_id
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS = 'RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS _SUCCESS';

export function receiveHpcUserLoadlevelerAbnormalJobsSuccess(response){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_FAILURE = 'RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS _FAILURE';

export function receiveHpcUserLoadlevelerAbnormalJobsFailure(error){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_FAILURE,
        error
    }
}

export function fetchHpcUserLoadlevelerAbnormalJobs(user, abnormal_jobs_id){
    return function (dispatch) {
        dispatch(requestHpcUserLoadlevelerStatus(user, abnormal_jobs_id));

        return $.getJSON('/api/v1/hpc/users/' + user + '/loadleveler/abnormal_jobs/' + abnormal_jobs_id, {},
            function(data){
            dispatch(
                receiveHpcUserLoadlevelerAbnormalJobsSuccess({
                    data: data
                })
            );
        });
    };
}

export const SET_HPC_USER_LOADLEVELER_SHOW_TYPE = "SET_HPC_USER_LOADLEVELER_SHOW_TYPE";
export function setHpcUserLoadLevelerShowType(show_type){
    return {
        type: SET_HPC_USER_LOADLEVELER_SHOW_TYPE,
        show_type
    }
}