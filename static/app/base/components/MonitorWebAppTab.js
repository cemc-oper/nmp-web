import React, { Component, PropTypes } from 'react';

export default class MonitorWebAppTab extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { active_item, tab_items } = this.props;
        let links = [];

        tab_items.map(function(tab_item, index){
            let class_name = "weui-tabbar__item";
            if(tab_item.name == active_item) {
                class_name += " weui-bar__item_on";
            }
            links.push(
                <a href={ tab_item.link } className={ class_name } key={ index }>
                    <img src={tab_item.icon} alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">{ tab_item.label }</p>
                </a>
            )

        });

        return (
            <div className="weui-tabbar">
                { links }
            </div>
        );
    }
}


MonitorWebAppTab.propTypes = {
    active_item: PropTypes.string.isRequired,
    tab_items: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        link: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        icon: PropTypes.string
    }))
};

MonitorWebAppTab.defaultProps = {
    active_item: 'operation-system',
    tab_items: [
        {
            'name':'operation-system',
            'link': '/',
            'label': '系统',
            'icon': '/static/image/icon_tabbar.png'
        },
        {
            'name':'hpc/disk',
            'link': '/hpc/nwp_xp/disk/usage',
            'label': '空间',
            'icon': '/static/image/icon_tabbar.png'
        },
        {
            'name':'hpc/loadleveler',
            'link': '/hpc/nwp_xp/loadleveler/status',
            'label': '队列',
            'icon': '/static/image/icon_tabbar.png'
        },
        {
            'name':'about',
            'link': '/about',
            'label': '关于',
            'icon': '/static/image/icon_tabbar.png'
        },
    ]
};


