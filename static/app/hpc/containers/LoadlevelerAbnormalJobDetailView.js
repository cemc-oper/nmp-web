import React, {Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import LoadlevelerJobUtil from '../util/LoadlevelerJobUtil'
import LoadlevelerJobDetail from '../components/LoadlevelerJobDetail'
import { TimeUtil } from '../../base/util/time'


class LoadlevelerAbnormalJobDetailView extends Component{
    render(){
        const { job_list, update_time, params } = this.props;
        const { job_id } = params;

        // find job in job_list
        let job = job_list.find(function(element, index, array){
            return LoadlevelerJobUtil.getPropTextById(element, "llq.id") === job_id;
        });
        let job_node = (
            <div>作业不存在：{job_id}</div>
        );
        if(job) {
            job_node = (
                <LoadlevelerJobDetail job={job} />
            )
        }

        return (
            <div>
                <div>
                    更新时间：{update_time}
                </div>
                { job_node }
            </div>
        )
    }
}

LoadlevelerAbnormalJobDetailView.propTypes = {
    job_list: PropTypes.arrayOf(PropTypes.shape({
        props: PropTypes.array
    })),
    update_time: PropTypes.string,
};

function mapStateToProps(state, ownProps){
    return {
        job_list: state.hpc.loadleveler_status.abnormal_jobs.abnormal_jobs,
        update_time: state.hpc.loadleveler_status.abnormal_jobs.update_time
    }
}

export default connect(mapStateToProps)(LoadlevelerAbnormalJobDetailView)