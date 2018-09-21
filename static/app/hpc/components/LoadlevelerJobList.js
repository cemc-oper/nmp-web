import { Component, PropTypes } from 'react';
import { Link } from 'react-router';

import LoadlevelerJobUtil from '../util/LoadlevelerJobUtil'


export default class LoadlevelerJobList extends Component{
    constructor(props){
        super(props);
        this.state = {
            sort_label: null,
            is_asc_order: true
        }
    }

    handleSortClick(sort_label){
        if(this.state.sort_label===null){
            this.setState({
                sort_label: sort_label,
                is_asc_order: true
            })
        } else if(this.state.sort_label === sort_label) {
            this.setState({
                is_asc_order: !this.state.is_asc_order
            });
        } else {
            this.setState({
                sort_label: sort_label
            })
        }
    }

    render(){
        const {job_list, base_location} = this.props;

        if(job_list===null)
        {
            return (
                <div>
                    <p>不存在</p>
                </div>
            )
        }

        let local_jobs = job_list.concat();
        local_jobs = LoadlevelerJobUtil.sortJobs(local_jobs, this.state.sort_label, this.state.is_asc_order);

        let jobs_nodes = local_jobs.map(function(a_job, index){
            let id = LoadlevelerJobUtil.getPropTextById(a_job, "llq.id");
            let node_link_url = base_location.pathname + "job_detail/" + id;
            let owner = LoadlevelerJobUtil.getPropTextById(a_job, "llq.owner");
            let queue_date = LoadlevelerJobUtil.getPropTextById(a_job, "llq.queue_date");
            let status = LoadlevelerJobUtil.getPropTextById(a_job, "llq.status");
            let ll_class = LoadlevelerJobUtil.getPropTextById(a_job, "llq.class");
            let job_script = LoadlevelerJobUtil.getPropTextById(a_job, "llq.job_script");
            return (
                <div className="weui-cell" key={index}>
                    <div className="weui-cell__bd">
                        <p className="loadleveler-status-row">
                            <span className="loadleveler-status-cell-status">
                                <Link to={node_link_url}>{status}</Link></span>
                            <span className="loadleveler-status-cell-owner">
                                <Link to={node_link_url}>{owner}</Link>
                            </span>
                            <span className="loadleveler-status-cell-class">
                                <Link to={node_link_url}>{ll_class}</Link></span>
                            <span className="loadleveler-status-cell-queue-date">
                                <Link to={node_link_url}>{queue_date}</Link></span>
                        </p>
                    </div>
                </div>
            );
        });

        return (
            <div className="weui-cells">
                <div className="weui-cell">
                    <div className="weui-cell__bd">
                        <p className="loadleveler-status-row">
                            <span className="loadleveler-status-cell-status">
                                <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.status")}
                                   className="loadleveler-status-header-button">ST</a>
                            </span>
                            <span className="loadleveler-status-cell-owner">
                                <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.owner")}
                                   className="loadleveler-status-header-button">Owner</a>
                            </span>
                            <span className="loadleveler-status-cell-class">
                                <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.class")}
                                   className="loadleveler-status-header-button">Class</a>
                            </span>
                            <span className="loadleveler-status-cell-queue-date">
                                <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.queue_date")}
                                   className="loadleveler-status-header-button">Queue Date</a>
                            </span>
                        </p>
                    </div>
                </div>
                { jobs_nodes }
            </div>
        )
    }
};

LoadlevelerJobList.propTypes = {
    job_list: PropTypes.arrayOf(
        PropTypes.shape({
            props: PropTypes.array
        })
    ),
    base_location: PropTypes.object
};

LoadlevelerJobList.defaultProps = {
    job_list: null
};