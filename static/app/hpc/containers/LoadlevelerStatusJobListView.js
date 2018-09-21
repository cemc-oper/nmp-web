import React, {PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadlevelerJobList from '../components/LoadlevelerJobList'
import { TimeUtil } from '../../base/util/time'


class LoadlevelerStatusJobListView extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const { job_queue } = this.props;
        if(job_queue===null)
        {
            return (
                <div>
                    <p>不存在</p>
                </div>
            )
        }

        const { job_list, update_time} = job_queue;

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

LoadlevelerStatusJobListView.propTypes = {
    job_queue: PropTypes.shape({
        update_time: PropTypes.string,
        job_list: PropTypes.arrayOf(PropTypes.shape({
            props: PropTypes.array
        }))
    }),
};

function mapStateToProps(state){
    return {
        job_queue: state.hpc.loadleveler_status.job_queue
    }
}

export default connect(mapStateToProps)(LoadlevelerStatusJobListView)