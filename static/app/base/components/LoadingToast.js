import React, { Component, PropTypes } from 'react';

export default class LoadingToast extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { content, shown, loading_style } = this.props;

        let loading_toast = (
            <div></div>
        );

        if(shown) {
            loading_toast = (
                <div id="loadingToast" style={ loading_style }>
                    <div className="weui-mask_transparent"></div>
                    <div className="weui-toast">
                        <i className="weui-loading weui-icon_toast" />
                        <p className="weui-toast__content">{ content }</p>
                    </div>
                </div>
            );
        }

        return (
            loading_toast
        );
    }
}


LoadingToast.propTypes = {
    content: PropTypes.string,
    shown: PropTypes.bool,
    loading_style: PropTypes.object
};

LoadingToast.defaultProps = {
    content: "数据加载中",
    shown: false,
    loading_style: {
        display:null
    }
};


