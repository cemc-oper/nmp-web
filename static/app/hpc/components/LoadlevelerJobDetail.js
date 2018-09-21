import { Component, PropTypes } from 'react';

import LoadlevelerJobUtil from '../util/LoadlevelerJobUtil'


export default class LoadlevelerJobDetail extends Component{
    constructor(props){
        super(props);
    }

    render(){
        const {job} = this.props;
        let id = LoadlevelerJobUtil.getPropTextById(job, "llq.id");
        let owner = LoadlevelerJobUtil.getPropTextById(job, "llq.owner");
        let queue_date = LoadlevelerJobUtil.getPropDataById(job, "llq.queue_date");
        let status = LoadlevelerJobUtil.getPropTextById(job, "llq.status");
        let ll_class = LoadlevelerJobUtil.getPropTextById(job, "llq.class");
        let job_script = LoadlevelerJobUtil.getPropTextById(job, "llq.job_script");

        let script_style = {
            "wordBreak": "break-all"
        };

        return (
            <div className="weui-cells">
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">ID</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div className="weui-input">{id}</div>
                    </div>
                </div>
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">owner</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div className="weui-input">{owner}</div>
                    </div>
                </div>
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">queue date</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div className="weui-input">{queue_date}</div>
                    </div>
                </div>
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">status</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div className="weui-input">{status}</div>
                    </div>
                </div>
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">class</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div className="weui-input">{ll_class}</div>
                    </div>
                </div>
                <div className="weui-cell">
                    <div className="weui-cell__hd">
                        <div className="weui-label">script</div>
                    </div>
                    <div className="weui-cell__bd">
                        <div style={script_style}>{job_script}</div>
                    </div>
                </div>
            </div>
        )
    }
};

LoadlevelerJobDetail.propTypes = {
    job: PropTypes.shape({
        props: PropTypes.array
    })
};

LoadlevelerJobDetail.defaultProps = {
    job: null
};