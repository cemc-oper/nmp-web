export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS';

export function requestOperationSystemRepoAbortedTasks(owner, repo, id){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS,
        owner,
        repo,
        id
    }
}

export function fetchOperationSystemRepoAbortedTasks(owner, repo, id) {
    return function (dispatch) {
        dispatch(requestOperationSystemRepoAbortedTasks(owner, repo, id));
        
        return $.getJSON('/api/v1/workflow/repos/' + owner + '/' + repo + '/aborted_tasks/' + id, {} ,function(data){
            dispatch(receiveOperationSystemRepoAbortedTasksSuccess({
                data: data
            }));
        });
    };
}


export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE';
export function receiveOperationSystemRepoAbortedTasksFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS';
export function receiveOperationSystemRepoAbortedTasksSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}



export const REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES = 'REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES';

export function requestOperationSystemRepoTaskCheckUnfitNodes(owner, repo, id){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES,
        owner,
        repo,
        id
    }
}

export function fetchOperationSystemRepoTaskCheckUnfitNodes(owner, repo, id) {
    return function (dispatch) {
        dispatch(requestOperationSystemRepoTaskCheckUnfitNodes(owner, repo, id));

        return $.getJSON('/api/v1/workflow/repos/' + owner + '/' + repo + '/task_check/unfit_nodes/' + id, {} ,function(data){
            dispatch(receiveOperationSystemRepoTaskCheckUnfitNodesSuccess({
                data: data
            }));
        });
    };
}


export const REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_FAILURE = 'REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_FAILURE';
export function receiveOperationSystemRepoTaskCheckUnfitNodesFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_SUCCESS = 'REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_SUCCESS';
export function receiveOperationSystemRepoTaskCheckUnfitNodesSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_TASK_CHECK_UNFIT_NODES_SUCCESS,
        response,
        receive_time: Date.now()
    }
}
