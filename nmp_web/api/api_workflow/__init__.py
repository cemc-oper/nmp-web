# coding: utf-8
from nmp_web.common.database import mongodb_client

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status

import nmp_web.api.api_workflow.status
import nmp_web.api.api_workflow.task_check
