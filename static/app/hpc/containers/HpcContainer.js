import React, { Component, PropTypes } from 'react';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'

class HpcContainer extends Component{
    render() {
        const { active_tab } = this.props;

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

HpcContainer.propTypes = {
    active_tab: PropTypes.string
};

HpcContainer.defaultProps = {
    active_tab: 'operation-system'
};
