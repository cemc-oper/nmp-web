import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import HpcDiskApp from './containers/HpcDiskApp'
import HpcDiskUsageApp from './containers/HpcDiskUsageApp'
import HpcDiskSpaceApp from './containers/HpcDiskSpaceApp'
import HpcLoadlevelerApp from './containers/HpcLoadlevelerApp'
import HpcLoadlevelerStatusApp from './containers/HpcLoadlevelerStatusApp'
import HpcLoadlevelerAbnormalJobsApp from './containers/HpcLoadlevelerAbnormalJobsApp'
import LoadlevelerAbnormalJobDetailView from './containers/LoadlevelerAbnormalJobDetailView'
import LoadlevelerAbnormalJobListView from './containers/LoadlevelerAbnormalJobListView'
import LoadlevelerStatusJobListView from './containers/LoadlevelerStatusJobListView'
import LoadlevelerStatusJobDetailView from './containers/LoadlevelerStatusJobDetailView'


export default (
    <Route path="/hpc" >
        <Route path=":user/disk" component={HpcDiskApp}>
            <Route path="usage" component={HpcDiskUsageApp} />
        </Route>
        <Route path="info/disk" component={HpcDiskApp}>
            <Route path="space" component={HpcDiskSpaceApp} />
        </Route>
        <Route path=":user/loadleveler" component={ HpcLoadlevelerApp } >

            <Route path="status" component={HpcLoadlevelerStatusApp} >
                <IndexRoute component={LoadlevelerStatusJobListView} />
                <Route path="job_detail/:job_id" component={LoadlevelerStatusJobDetailView} />
            </Route>

            <Route path="abnormal_jobs/:abnormal_jobs_id" component={HpcLoadlevelerAbnormalJobsApp} >
                <IndexRoute component={LoadlevelerAbnormalJobListView} />
                <Route path="job_detail/:job_id" component={LoadlevelerAbnormalJobDetailView} />
            </Route>
        </Route>
    </Route>
)