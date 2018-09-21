import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchHpcUserLoadlevelerStatus,
} from '../actions/loadleveler_status';

import LoadingToast from '../../base/components/LoadingToast'

import { TimeUtil } from '../../base/util/time'
import LoadlevelerJobList from '../components/LoadlevelerJobList'

export class HpcLoadlevelerStatusApp extends Component{
    constructor(props){
        super(props);
        this.state = {
            sort_label: null,
            is_asc_order: true
        }
    }

    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        dispatch(fetchHpcUserLoadlevelerStatus(user));
    }

    render() {
        const { params, status } = this.props;

        let user = params.user;

        return (
            <div>
                <h1 className="page_title">LoadLeveler队列</h1>
                { this.props.children }
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

HpcLoadlevelerStatusApp.propTypes = {
    status: PropTypes.object
};

function mapStateToProps(state){
    return {
        status: state.hpc.loadleveler_status.status
    }
}

export default connect(
    mapStateToProps
)(HpcLoadlevelerStatusApp)