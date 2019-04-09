export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS';

export function requestOperationSystemOwnerRepos(owner){
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS,
        owner
    }
}

export function fetchOperationSystemOwnerRepos(owner) {
    return function (dispatch) {
        dispatch(requestOperationSystemOwnerRepos(owner));
        // return fetch('/api/v1/operation-systems/owners/' + owner + '/repos')
        //     .then(response => response.json())
        //     .then(data => dispatch(receiveOperationSystemOwnerReposSuccess({
        //             data: data
        //     })));
        return $.getJSON('/api/v1/workflow/owners/' + owner + '/repos', {} ,function(data){
            dispatch(receiveOperationSystemOwnerReposSuccess({
                data: data
            }));
        });
    };
}


export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE';
export function receiveOperationSystemOwnerReposFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOperationSystemOwnerReposSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}




export const REQUEST_OPERATION_SYSTEM_REPO_STATUS = 'REQUEST_OPERATION_SYSTEM_REPO_STATUS';

export function requestOperationSystemRepoStatus(owner, repo, path){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_STATUS,
        owner,
        repo,
        path
    }
}

export function fetchOperationSystemRepoStatus(owner, repo, path) {
    return function (dispatch) {
        dispatch(requestOperationSystemRepoStatus(owner, repo, path));
        // return fetch('/api/v1/operation-systems/repos/' + owner + '/' + repo + '/status/head' + path)
        //     .then(response => response.json())
        //     .then(data => dispatch(receiveOperationSystemRepoStatusSuccess({
        //             data: data
        //     })));

        return $.getJSON('/api/v1/workflow/repos/' + owner + '/' + repo + '/status/head' + path, {} ,function(data){
            dispatch(receiveOperationSystemRepoStatusSuccess({
                data: data
            }));
        });
    };
}


export const REQUEST_OPERATION_SYSTEM_REPO_STATUS_FAILURE = 'REQUEST_OPERATION_SYSTEM_REPO_STATUS_FAILURE';
export function receiveOperationSystemRepoStatusFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_STATUS_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS = 'REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOperationSystemRepoStatusSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}