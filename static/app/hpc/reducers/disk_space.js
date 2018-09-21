import {
    REQUEST_HPC_DISK_SPACE,
    RECEIVE_HPC_DISK_SPACE_SUCCESS
} from '../actions/disk_space'


export function disk_space_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    file_systems: [],
    time: null
}, action) {
    switch (action.type) {
        case REQUEST_HPC_DISK_SPACE:
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                },
            });
        case RECEIVE_HPC_DISK_SPACE_SUCCESS:
            let file_systems = action.response.data.message.data.response.file_systems;

            file_systems.sort(function(a,b){
                let a_file_system = a.file_system.toUpperCase();
                let b_file_system = b.file_system.toUpperCase();
                if( a_file_system < b_file_system){
                    return -1;
                } else if(a_file_system > b_file_system){
                    return 1;
                } else {
                    return 0;
                }
            });

            return Object.assign({}, state, {
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                file_systems: file_systems,
                time: action.response.data.message.time,
            });
        default:
            return state;
    }
}
