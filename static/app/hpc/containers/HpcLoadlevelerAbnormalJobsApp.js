import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadingToast from '../../base/components/LoadingToast'

import { fetchHpcUserLoadlevelerAbnormalJobs} from '../actions/loadleveler_status';

class HpcLoadlevelerAbnormalJobsApp extends Component{
    constructor(props){
        super(props);
    }

    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;
        let abnormal_jobs_id = params.abnormal_jobs_id;

        dispatch(fetchHpcUserLoadlevelerAbnormalJobs(user, abnormal_jobs_id));
    }

    render() {
        const { params, status } = this.props;
        return (
            <div>
                <h1 className="page_title">Loadleveler异常任务</h1>
                { this.props.children }
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

HpcLoadlevelerAbnormalJobsApp.propTypes = {
    status: PropTypes.shape({
        is_fetching: PropTypes.bool,
        last_updated: PropTypes.oneOfType([
            null,
            PropTypes.number
        ])
    })
};

function mapStateToProps(state){
    return {
        status: state.hpc.loadleveler_status.status
    }
}

export default connect(mapStateToProps)(HpcLoadlevelerAbnormalJobsApp)