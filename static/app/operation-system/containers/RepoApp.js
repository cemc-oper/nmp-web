import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class RepoApp extends Component{
    componentDidMount(){
    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        return (
            <div>
                <h1 className="page_title">
                    <a href={ "/" + owner }>{ owner }</a>
                    /
                    <a href={ "/" + owner + "/" + repo }>{ repo }</a>
                </h1>
                { this.props.children }
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoApp)