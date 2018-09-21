import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'

class HpcApp extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { params } = this.props;
        let active_tab = "hpc/disk";

        return (
            <div className="container">
                <div className="weui-tab">
                    <div className="weui-tab__panel">
                        {this.props.children}
                    </div>

                    <MonitorWebAppTab active_item={ active_tab }/>
                </div>
            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(HpcApp)
