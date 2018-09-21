import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {REQUEST_USER_INFO, RECEIVE_USER_INFO} from '../actions/index'

function welcome_reducer(state={
    user: {
        info: {}
    }
}, action){
    switch(action.type){
        case RECEIVE_USER_INFO:
            let data = action.response.data;
            let user_info = {};
            if(data['status'] === 'ok'){
                user_info = action.response.data.user_info;
            }
            return new Object({
                user: {
                    info: user_info
                }
            });
            break;
        default:
            return state;
    }
}

const welcomeAppReducer = combineReducers({
    welcome:welcome_reducer,
    routing
});

export default welcomeAppReducer;