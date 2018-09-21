import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { NodeStatusImage } from '../../base/components/NodeStatusImage'
import LoadingToast from '../../base/components/LoadingToast'

import { fetchOperationSystemRepoStatus } from '../actions/owner';
import { TimeUtil } from '../../base/util/time'

class RepoStatusApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        let repo = params.repo;
        let path = '/';
        if(params.hasOwnProperty('splat'))
            path += params.splat;

        dispatch(fetchOperationSystemRepoStatus(owner, repo, path));
    }

    render() {
        const { params, node_status, status } = this.props;
        if(node_status===null)
        {
            return (
                <div>
                    <p>不存在</p>
                    <LoadingToast shown={ status.is_fetching } />
                </div>
            )
        }

        let owner = params.owner;
        let repo = params.repo;
        let path = '/';
        if(params.hasOwnProperty('splat'))
            path += params.splat;

        let repo_last_update_time = '未知';
        let cur_time = new Date();
        if(node_status['last_updated_time']!==null) {
            let last_updated_time = new Date(node_status['last_updated_time']);
            repo_last_update_time = TimeUtil.getDelayTime(TimeUtil.parseDate(last_updated_time), TimeUtil.parseDate(cur_time));
        }

        let children_node = node_status['children'].map(function(a_child, i){
            let a_child_status = "unk";
            if(a_child['status']!==null)
                a_child_status = a_child['status'];

            return (
                <a className="weui-cell" key={i} href={ "/" + owner + "/" + repo + "/status/head" + a_child['path'] } >
                    <div className="weui-cell__hd">
                        <NodeStatusImage node_status={a_child_status} />
                    </div>

                    <div className="weui-cell__bd">
                        <p>{ a_child['name'] }</p>
                    </div>

                    <div className="weui-cell__ft">
                    </div>
                    <LoadingToast shown={ status.is_fetching } />
                </a>
            )
        });

        return (
            <div>
                <p>更新时间：{ repo_last_update_time }</p>
                <p>当前路径：{ path }</p>

                <div className="weui-cells weui-cells_access">
                    { children_node }
                </div>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

RepoStatusApp.propTypes = {
    node_status: PropTypes.shape({
        last_updated_time: PropTypes.string,
        owner: PropTypes.string,
        repo: PropTypes.string,
    }),
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
        node_status: state.operation_system.repo.node_status,
        status: state.operation_system.repo.status
    }
}

export default connect(mapStateToProps)(RepoStatusApp)