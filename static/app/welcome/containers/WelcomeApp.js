import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'

class WelcomeApp extends Component{
    constructor(props) {
        super(props);
        this.state = {
            owner: ''
        }
    }

    onChange(e) {
        this.setState({owner: e.target.value});
    }

    handleClick(e) {
        e.preventDefault();
        console.log(this.state.owner);
        window.location.href='/'+this.state.owner;
    }

    render() {
        const { params } = this.props;

        let tab_bar_item_name = "operation-system";

        return (
            <div className="container">
                <div className="weui-tab">
                    <div className="weui-tab__panel">
                        <h1 className="page_title">NWPC 业务运行监控</h1>
                        <div className="weui-grids">
                            <a href="/nwp_xp" className="weui-grid">
                                <p className="weui-grid__label">
                                    运行科
                                </p>
                            </a>
                            <a href="/nwp_pos" className="weui-grid">
                                <p className="weui-grid__label">
                                    产品科
                                </p>
                            </a>
                            <a href="/nwp_vfy" className="weui-grid">
                                <p className="weui-grid__label">
                                    检验科
                                </p>
                            </a>
                        </div>

                        <div className="weui-cells__title">访问</div>
                        <div className="weui-cells weui-cells_form">
                            <div className="weui-cell">
                                <div className="weui-cell__hd">
                                    <label className="weui-label">owner</label>
                                </div>
                                <div className="weui-cell__bd weui-cell_primary">
                                    <input id="owner_name_input" className="weui-input" type="tel" placeholder="请输入用户名"
                                           onChange={this.onChange.bind(this)} value={this.state.owner} />
                                </div>
                            </div>
                        </div>
                        <div className="button_sp_area">
                            <a id="go_to_page_link" href="javascript:;" className="weui-btn weui-btn_plain-primary"
                               onClick={this.handleClick.bind(this)}>
                                访问
                            </a>
                        </div>
                        {this.props.children}
                    </div>

                    <MonitorWebAppTab active_item={ tab_bar_item_name }/>
                </div>
            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(WelcomeApp)
