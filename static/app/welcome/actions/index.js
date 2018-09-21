export const REQUEST_USER_INFO = "REQUEST_USER_INFO";

export function requestUserInfo(){
    return {
        type: REQUEST_USER_INFO
    }
}

export const RECEIVE_USER_INFO = "RECEIVE_USER_INFO";

export function receiveUserInfo(response){
    return {
        type: RECEIVE_USER_INFO,
        response,
        receive_time: Date.now()
    }
}

export function fetchUserInfo(){
    return function (dispatch){
        dispatch(requestUserInfo());
        return $.getJSON(
            '/api/v1/user/info',
            {},
            function(data){
                dispatch(receiveUserInfo({
                    data: data
                }))
            }
        )
    };
}
