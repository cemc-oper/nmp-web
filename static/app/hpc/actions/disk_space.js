export const REQUEST_HPC_DISK_SPACE = 'REQUEST_HPC_DISK_SPACE';

export function requestHpcDiskSpace(hpc){
    return {
        type: REQUEST_HPC_DISK_SPACE,
        hpc
    }
}

export function fetchHpcDiskSpace(hpc) {
    return function (dispatch) {
        dispatch(requestHpcDiskSpace(hpc));
        
        return $.getJSON('/api/v1/hpc/' +hpc +'/disk/space', {} ,function(data){
            dispatch(
                receiveHpcUserDiskSpaceSuccess({
                    data: data
                })
            );
        });
    };
}


export const RECEIVE_HPC_DISK_SPACE_FAILURE = 'RECEIVE_HPC_DISK_SPACE_FAILURE';
export function receiveHpcDiskSpaceFailure(error){
    return {
        type: RECEIVE_HPC_DISK_SPACE_FAILURE,
        error
    }
}


export const RECEIVE_HPC_DISK_SPACE_SUCCESS = 'RECEIVE_HPC_DISK_SPACE_SUCCESS';
export function receiveHpcUserDiskSpaceSuccess(response) {
    return {
        type: RECEIVE_HPC_DISK_SPACE_SUCCESS,
        response,
        receive_time: Date.now()
    }
}
