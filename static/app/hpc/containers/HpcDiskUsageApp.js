import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchAddHpcUserDiskUsage,
    clearHpcDiskUsageUsers
} from '../actions/disk_usage';

import LoadingToast from '../../base/components/LoadingToast'
import FileSystemUsagePieChart, {FileSystemUsagePieChartLegend} from '../../base/components/FileSystemUsagePieChart'

import { TimeUtil } from '../../base/util/time'

class HpcDiskUsageApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        // dispatch(clearHpcDiskUsageUsers());
        dispatch(fetchAddHpcUserDiskUsage("nwp_sp"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_xp"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_pd"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_qu"));
        dispatch(fetchAddHpcUserDiskUsage("nwp"));
    }

    render() {
        const { params, disk_usage } = this.props;

        let label_style = {
            alignItems: 'center',
            display: 'flex'
        };

        let disk_usage_list = [];
        disk_usage.users.map(function(a_disk_usage, index){
            let file_systems = a_disk_usage.file_systems;

            let file_systems_group = [];

            let chunk_size = 3;

            for(let i=0, j=file_systems.length; i < j; i+=chunk_size)
            {
                file_systems_group.push(
                    file_systems.slice(i, i+chunk_size)
                )
            }

            let file_systems_group_node = [];
            file_systems_group.map(function(a_group, group_index){
                let file_systems_node = [];
                a_group.map(function(a_file_system, file_index){
                    file_systems_node.push(
                        <span className="disk-usage-cell" key={file_index}>
                            <FileSystemUsagePieChart data={
                            {
                                label: a_file_system.file_system,
                                usage: a_file_system.block_limits.current,
                                total: a_file_system.block_limits.quota
                            }
                            }/>
                        </span>
                    )
                });
                file_systems_group_node.push(
                    <div className="disk-usage-row" key={group_index}>
                        { file_systems_node }
                    </div>
                );
            });

            disk_usage_list.push(
                <div key={index}>
                    <h2>{ a_disk_usage.user }</h2>
                    <p>更新时间：{ TimeUtil.getDelayTime(TimeUtil.parseUTCTimeString(a_disk_usage.time), TimeUtil.getNow())} </p>
                    <div className="disk-usage-box">
                        { file_systems_group_node }
                    </div>
                </div>
            )
        });

        let link_box_style = {
            display: 'flex',
            justifyContent: 'flex-end'
        };

        return (
            <div>
                <h1 className="page_title">业务账户磁盘限额</h1>
                <div style={link_box_style}>
                    <div className="button-sp-area">
                        <a href="/hpc/info/disk/space" className="weui-btn weui-btn_mini weui-btn_default">查看磁盘空间</a>
                    </div>
                </div>
                <FileSystemUsagePieChartLegend/>
                { disk_usage_list }
                <LoadingToast shown={ disk_usage.status.is_fetching } />
            </div>
        );
    }
}

HpcDiskUsageApp.propTypes = {
    disk_usage: PropTypes.object
};

function mapStateToProps(state){
    return {
        disk_usage: state.hpc.disk_usage
    }
}

export default connect(mapStateToProps)(HpcDiskUsageApp)