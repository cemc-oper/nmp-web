import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { NodeStatusImage } from '../../base/components/NodeStatusImage'
import LoadingToast from '../../base/components/LoadingToast'

import { fetchOperationSystemRepoTaskCheckUnfitNodes } from '../actions/repo';
import { TimeUtil } from '../../base/util/time'

class RepoTaskCheckUnfitNodesApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        let repo = params.repo;
        let unfit_nodes_id = params.unfit_nodes_id;

        dispatch(fetchOperationSystemRepoTaskCheckUnfitNodes(owner, repo, unfit_nodes_id));
    }

    render() {
        const { params, unfit_nodes, status } = this.props;
        if(unfit_nodes===null)
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
        let unfit_nodes_id = params.unfit_nodes_id;

        let repo_last_update_time = '未知';
        let cur_time = TimeUtil.getUTCNow();
        if(unfit_nodes['check_time']!==null) {
            repo_last_update_time = TimeUtil.getDelayTime(
                TimeUtil.parseUtcIsoTimeString(unfit_nodes['check_time']), cur_time);
        }

        let image_style = {
            width:'30px',
            marginRight: '5px'
        };

        let task_nodes = unfit_nodes['unfit_nodes'].map(function(a_node, i){
            let unfit_check_list_node = a_node['check_results'].map(function(an_unfit_check, i) {
                if(an_unfit_check['_cls'] === 'StatusCheckResult' ){
                    let expected_value = an_unfit_check['expected_value'];

                    let expected_value_node = (<div/>);
                    if(expected_value['operator'] === "in"){
                        expected_value_node = expected_value['fields'].map(function(a_status,i){
                            return (<NodeStatusImage node_status={ a_status } image_style={ image_style } />)
                        });
                    }

                    return(
                        <div className="weui-flex">
                            <div className="weui-flex__item">
                                <div className="placeholder">节点状态</div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">
                                    <NodeStatusImage node_status={ an_unfit_check['value'] } image_style={ image_style } />
                                </div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">
                                    {expected_value_node}
                                </div>
                            </div>
                        </div>
                    )
                } else if (an_unfit_check['_cls'] === 'VariableCheckResult') {
                    return (
                        <div className="weui-flex">
                            <div className="weui-flex__item">
                                <div className="placeholder">{an_unfit_check['variable_name']}</div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">{an_unfit_check['value']}</div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">{an_unfit_check['expected_value']}</div>
                            </div>
                        </div>
                    )
                }
            });
            return (
                <div className="unfit-node-path-row" key={i} >
                    <h2 className="node-path">
                        { a_node['node_path'] }
                    </h2>
                    <div>
                        <div className="weui-flex">
                            <div className="weui-flex__item">
                                <div className="placeholder">项目</div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">实际</div>
                            </div>
                            <div className="weui-flex__item">
                                <div className="placeholder">期望</div>
                            </div>
                        </div>
                        { unfit_check_list_node }
                    </div>
                </div>
            )
        });

        return (
            <div>
                <p>更新时间：{ repo_last_update_time }</p>

                <article className="weui-article">
                    <section>
                        <h1>异常节点</h1>
                        { task_nodes }
                    </section>
                </article>

                <div className="weui-cells__title">链接</div>
                <div className="weui-cells weui-cells_access">
                    <a className="weui-cell" href={ "/" +  owner  + "/" +  repo }>
                        <div className="weui-cell__bd weui-cell_primary">
                            <p>最新状态</p>
                        </div>
                        <div className="weui-cell__ft">
                        </div>
                    </a>
                </div>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

RepoTaskCheckUnfitNodesApp.propTypes = {
    unfit_nodes: PropTypes.shape({
        collected_time: PropTypes.string,
        status_blob_id: PropTypes.number,
        unfit_nodes: PropTypes.arrayOf(PropTypes.shape({
            node_path: PropTypes.string,
            check_results: PropTypes.array
        })),
        name: PropTypes.string,
        trigger: PropTypes.array,
        update_time: PropTypes.string
    })
};

function mapStateToProps(state){
    return {
        unfit_nodes: state.operation_system.repo.task_check.unfit_nodes,
        status: state.operation_system.repo.status
    }
}

export default connect(mapStateToProps)(RepoTaskCheckUnfitNodesApp)