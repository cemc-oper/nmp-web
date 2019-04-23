import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'
import {fetchUserInfo} from '../actions/index'

class AboutApp extends Component{
    constructor(props) {
        super(props);
        this.state = {
            owner: ''
        }
    }

    componentDidMount(){
        const { dispatch } = this.props;
        dispatch(fetchUserInfo());
    }

    onChange(e) {
        this.setState({owner: e.target.value});
    }

    handleClick(e) {
        e.preventDefault();
        //console.log(this.state.owner);
        window.location.href='/'+this.state.owner;
    }

    getUserType() {
        const { user } = this.props;
        if(user.info.hasOwnProperty('UserId')){
            return 'member';
        } else if(user.info.hasOwnProperty('OpenId')){
            return 'visitor'
        }else {
            return 'anonymous'
        }
    }

    render() {
        const { params, user } = this.props;
        let user_type = this.getUserType();
        let user_info = null;
        switch(user_type){
            case 'member':
                user_info = (
                    <p>{user.info.UserId}</p>
                );
                break;
            case 'visitor':
                user_info = (
                    <p>{user.info.OpenId}</p>
                );
                break;
            case 'anonymous':
            default:
                user_info = (
                    <p>尚未登录，<a href="/login">点击登录</a></p>
                );

        }

        let tab_bar_item_name = "about";

        return (
            <div className="container">
                <div className="weui-tab">
                    <div className="weui-tab__panel">
                        <article className="weui-article">
                            <h1>关于</h1>
                            <section>
                                <h2 className="title">当前用户</h2>
                                <p>{user_info}</p>
                            </section>
                            <section>
                                <h2 className="title">开发者</h2>
                                <p>perillaroc</p>
                            </section>
                        </article>
                    </div>

                    <MonitorWebAppTab active_item={ tab_bar_item_name }/>
                </div>
            </div>
        );
    }
}

AboutApp.propTypes = {
    user: (PropTypes.shape({
        info : PropTypes.object
    }))
};

AboutApp.defaultProps = {
    user: {
        info: {

        }
    }
};


function mapStateToProps(state){
    return {
        user: state.welcome.user
    }
}

export default connect(mapStateToProps)(AboutApp)
