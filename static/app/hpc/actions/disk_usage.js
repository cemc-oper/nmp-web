export const REQUEST_ADD_HPC_USER_DISK_USAGE = 'REQUEST_ADD_HPC_USER_DISK_USAGE';

export function requestAddHpcUserDiskUsage(user){
    return {
        type: REQUEST_ADD_HPC_USER_DISK_USAGE,
        user
    }
}

export function fetchAddHpcUserDiskUsage(user) {
    return function (dispatch) {
        dispatch(requestAddHpcUserDiskUsage(user));
        
        return $.getJSON('/api/v1/hpc/users/' + user + '/disk/usage', {} ,function(data){
            dispatch(
                receiveAddHpcUserDiskUsageSuccess({
                    data: data
                })
            );
        });
    };
}


export const ADD_HPC_USER_DISK_USAGE_FAILURE = 'ADD_HPC_USER_DISK_USAGE_FAILURE';
export function receiveAddHpcUserDiskUsageFailure(error){
    return {
        type: ADD_HPC_USER_DISK_USAGE_FAILURE,
        error
    }
}


export const ADD_HPC_USER_DISK_USAGE_SUCCESS = 'ADD_HPC_USER_DISK_USAGE_SUCCESS';
export function receiveAddHpcUserDiskUsageSuccess(response) {
    return {
        type: ADD_HPC_USER_DISK_USAGE_SUCCESS,
        response,
        receive_time: Date.now()
    }
}

// clear

export const CLEAR_HPC_DISK_USAGE_USERS = 'CLEAR_HPC_DISK_USAGE_USERS';

export function clearHpcDiskUsageUsers(){
    return {
        type: CLEAR_HPC_DISK_USAGE_USERS
    }
}