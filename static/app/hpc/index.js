// import 'babel-polyfill'

import React from 'react'
import { render } from 'react-dom'

import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'

import { browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'


import operationSystemAppReducer from './reducers'

import Root from './containers/Root'


const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
    operationSystemAppReducer, /* preloadedState, */
    composeEnhancers(
        applyMiddleware(
            thunkMiddleware
        )
    )
);

const history = syncHistoryWithStore(browserHistory, store);

render(
    <Root store={store} history={history} />,
    document.getElementById('app')
);
