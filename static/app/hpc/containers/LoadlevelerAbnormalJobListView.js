import React, {PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadlevelerJobList from '../components/LoadlevelerJobList'
import { TimeUtil } from '../../base/util/time'


class LoadlevelerAbnormalJobListView extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const { abnormal_jobs } = this.props;
        if(abnormal_jobs===null)
        {
            return (
                <div>
                    <p>不存在</p>
                </div>
            )
        }

        const { abnormal_jobs:job_list, update_time} = abnormal_jobs;

        let last_update_time = '未知';
        let cur_time = TimeUtil.getUTCNow();
        if(update_time!==null) {
            last_update_time = TimeUtil.getDelayTime(
                TimeUtil.parseUtcIsoTimeString(update_time), cur_time);
        }

        return (
            <div>
                <p>更新时间：{ last_update_time } </p>
                <LoadlevelerJobList
                    job_list={job_list}
                    base_location={this.props.location}
                />
            </div>
        )
    }
}

LoadlevelerAbnormalJobListView.propTypes = {
    abnormal_jobs: PropTypes.shape({
        update_time: PropTypes.string,
        abnormal_jobs_id: PropTypes.number,
        abnormal_jobs: PropTypes.arrayOf(PropTypes.shape({
            props: PropTypes.array
        })),
        plugins: PropTypes.array
    }),
};

function mapStateToProps(state){
    return {
        abnormal_jobs: state.hpc.loadleveler_status.abnormal_jobs
    }
}

export default connect(mapStateToProps)(LoadlevelerAbnormalJobListView)