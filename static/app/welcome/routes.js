import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import WelcomeApp from './containers/WelcomeApp'
import AboutApp from './containers/AboutApp'

export default (
    <Route path="/">
        <IndexRoute component={WelcomeApp} />
        <Route path="about" component={AboutApp} />
    </Route>
)