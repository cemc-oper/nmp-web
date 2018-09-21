import React, { Component, PropTypes } from 'react';
import echarts from 'echarts'

import elementResizeEvent from 'element-resize-event';

export default class FileSystemUsagePieChart extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        let echarts_instance = echarts.init(this.refs.chart_dom);
        this.renderChartDom();

        elementResizeEvent(this.refs.chart_dom, function() {
            echarts_instance.resize();
        });
    }

    componentDidUpdate(){
        this.renderChartDom();
    };

    componentWillUnmount(){
        echarts.dispose(this.refs.chart_dom);
    }

    getEchartsInstance(){
        return echarts.getInstanceByDom(this.refs.chart_dom);
    }

    getUsedColor(value){
        const { config } = this.props;
        if(config.warning.inRange(value)){
            return config.warning.used_color;
        } else if(config.normal.inRange(value)){
            return config.normal.used_color;
        } else {
            return 'rgb(0,0,0)';
        }
    }

    getFreeColor(value){
        const { config } = this.props;
        if(config.warning.inRange(value)){
            return config.warning.free_color;
        } else {
            return config.normal.free_color;
        }
    }

    renderChartDom(){
        const { data, config } = this.props;
        let { label, usage, total } = data;

        // // over the quota
        // if (usage>total){
        //    usage = total;
        // }
        let echarts_instance = this.getEchartsInstance();

        echarts_instance.setOption({
            title:{
                text: label,
                top: 'center',
                left: 'center',
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 15
                }
            },
            series: [
                {
                    'name': '使用情况',
                    type: 'pie',
                    radius: [ '50%', '70%' ],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        }
                    },
                    data: [
                        {
                            value: usage,
                            name:'使用',
                            itemStyle: {
                                normal: {
                                    color: this.getUsedColor(usage/total)
                                }
                            }
                        },
                        {
                            value: total-usage,
                            name: '空闲',
                            itemStyle: {
                                normal: {
                                    color: this.getFreeColor(usage/total)
                                }
                            }

                        }
                    ]
                }
            ]
        });
        return echarts_instance;
    }

    render() {
        const { data } = this.props;
        let chart_style = {
            height: 150
        };

        return (
            <div ref="chart_dom" style={ chart_style }>

            </div>
        )
    }
}

FileSystemUsagePieChart.propTypes = {
    data: PropTypes.shape({
        label: PropTypes.string,
        usage: PropTypes.number,
        total: PropTypes.number
    }),
    config: PropTypes.object
};

FileSystemUsagePieChart.defaultProps = {
    config: {
        normal: {
            used_color: 'rgb(49,163,84)',
            free_color: 'rgb(247,252,185)',
            inRange: function(value){
                let min = 0;
                let max = 0.9;
                return value>=min && value<max
            }
        },
        warning: {
            used_color: 'rgb(240,59,32)',
            free_color: 'rgb(247,252,185)',
            inRange: function(value){
                let min = 0.9;
                let max = 1.0;
                return value>=min && value<=max
            }
        }
    },
};

export class FileSystemUsagePieChartLegend extends Component {
    constructor(props){
        super(props);
    }

    componentDidMount(){
        let echarts_instance = echarts.init(this.refs.chart_dom);
        this.renderChartDom();

        elementResizeEvent(this.refs.chart_dom, function() {
            echarts_instance.resize();
        });
    }

    componentDidUpdate(){
        this.renderChartDom();
    };

    componentWillUnmount(){
        echarts.dispose(this.refs.chart_dom);
    }

    getEchartsInstance(){
        return echarts.getInstanceByDom(this.refs.chart_dom);
    }

    renderChartDom(){
        let { config } = this.props;
        let { legend } = config;
        let echarts_instance = this.getEchartsInstance();

        let series = legend.map(function(item, index){
            return {
                name: item.name,
                type: 'bar',
                stack: '总量',
                itemStyle: {
                    normal: {
                        color: item.color
                    }
                },
                data: [item.value]
            }
        });

        echarts_instance.setOption({
            grid:{
                show:false
            },
            xAxis:  {
                type: 'value',
                splitLine:{
                    show:false
                },
                splitNumber: 10,
                axisLabel: {
                    formatter: '{value}'
                }
            },
            yAxis: {
                type: 'category',
                data: [''],
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
            },
            series: series
        });
        return echarts_instance;
    }

    render(){
        const { data } = this.props;
        let chart_style = {
            height: 100
        };

        return (
            <div>
                <div>图例：使用百分比</div>
                <div ref="chart_dom" style={ chart_style }>

                </div>
            </div>

        )
    }
}

FileSystemUsagePieChartLegend.propTypes = {
    config:PropTypes.shape({
        legend: PropTypes.arrayOf(
            PropTypes.shape({
                name :PropTypes.string,
                color: PropTypes.string,
                value: PropTypes.number
            })
        )
    })
};

FileSystemUsagePieChartLegend.defaultProps = {
    config: {
        legend: [
            {
                name: '正常',
                color: 'rgb(49,163,84)',
                value: 90
            },
            {
                name: '警告',
                color: 'rgb(240,59,32)',
                value: 10
            }
        ]
    }
};