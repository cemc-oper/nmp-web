import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { fetchOperationSystemOwnerRepos } from '../actions/owner';

import { TimeUtil } from '../../base/util/time'
import { NodeStatusImage } from '../../base/components/NodeStatusImage'
import LoadingToast from '../../base/components/LoadingToast'

export class OwnerApp extends Component{

    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        dispatch(fetchOperationSystemOwnerRepos(owner));
    }

    render() {
        const { params, repos_status, status } = this.props;
        let owner = params.owner;
        let cur_time = new Date();

        let repos = repos_status.map(function(a_repo, i){
            let repo_status = "unk";
            if(a_repo['status']!==null)
                repo_status = a_repo['status'];

            let repo_last_update_time = '未知';
            if(a_repo['last_updated_time']!==null) {
                let last_updated_time = new Date(a_repo['last_updated_time']);
                repo_last_update_time = TimeUtil.getDelayTime(
                    TimeUtil.parseDate(last_updated_time),
                    TimeUtil.parseDate(cur_time)
                );
            }

            return (
                <a className="weui-cell" key={i} href={ "/" + owner + "/" + a_repo['repo'] }>
                    <div className="weui-cell__hd">
                        <NodeStatusImage node_status={repo_status} />
                    </div>
                    <div className="weui-cell__bd weui-cell_primary">
                        <p>{ a_repo['repo'] }</p>
                    </div>
                    <div className="weui-cell__ft">
                        { repo_last_update_time}
                    </div>
                    <LoadingToast shown={ status.is_fetching } />
                </a>
            )
        });

        return (
            <div>
                <h1 className="page_title"><a href={ "/" + owner } >{ owner }</a></h1>
                <div className="weui-cells weui-cells_access">
                    { repos }
                </div>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

OwnerApp.propTypes = {
    repos_status: PropTypes.arrayOf(PropTypes.shape({
        last_updated_time: PropTypes.string,
        owner: PropTypes.string,
        repo: PropTypes.string,
    })),
    status: PropTypes.shape({
        is_fetching: PropTypes.bool,
        last_updated: PropTypes.oneOfType([
            PropTypes.null,
            PropTypes.number
        ])
    })
};

function mapStateToProps(state){
    return {
        repos_status: state.operation_system.owner.repos_status,
        status: state.operation_system.owner.status
    }
}

export default connect(mapStateToProps)(OwnerApp)