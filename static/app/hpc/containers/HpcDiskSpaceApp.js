import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchHpcDiskSpace
} from '../actions/disk_space';

import LoadingToast from '../../base/components/LoadingToast'
import FileSystemUsagePieChart, {FileSystemUsagePieChartLegend} from '../../base/components/FileSystemUsagePieChart'

import { TimeUtil } from '../../base/util/time'

class HpcDiskSpaceApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        dispatch(fetchHpcDiskSpace("info"));
    }

    render() {
        const { params, disk_space } = this.props;

        let label_style = {
            alignItems: 'center',
            display: 'flex'
        };

        let file_systems_group = [];
        let chunk_size = 3;

        for(let i=0, j=disk_space.file_systems.length; i < j; i+=chunk_size)
        {
            file_systems_group.push(
                disk_space.file_systems.slice(i, i+chunk_size)
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
                                    usage: a_file_system.gb_blocks - a_file_system.free_space,
                                    total: a_file_system.gb_blocks
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

        let link_box_style = {
            display: 'flex',
            justifyContent: 'flex-end'
        };
        return (
            <div>
                <h1 className="page_title">HPC磁盘空间</h1>
                <div style={link_box_style}>
                    <div className="button-sp-area">
                        <a href="/hpc/nwp_xp/disk/usage" className="weui-btn weui-btn_mini weui-btn_default">查看账户限额</a>
                    </div>
                </div>
                <FileSystemUsagePieChartLegend/>
                <div>
                    <p>更新时间：{ TimeUtil.getDelayTime(TimeUtil.parseUTCTimeString(disk_space.time), TimeUtil.getNow())} </p>
                    <div className="disk-usage-box">
                        { file_systems_group_node }
                    </div>
                </div>
                <LoadingToast shown={ disk_space.status.is_fetching } />
            </div>
        );
    }
}

HpcDiskSpaceApp.propTypes = {
    disk_space: PropTypes.object
};

function mapStateToProps(state){
    return {
        disk_space: state.hpc.disk_space
    }
}

export default connect(mapStateToProps)(HpcDiskSpaceApp)