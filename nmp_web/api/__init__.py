# coding=utf-8
from flask import Blueprint

api_app = Blueprint('api_app', __name__, template_folder='template')

import nmp_web.api.hpc
import nmp_web.api.workflow
import nmp_web.api.workload
import nmp_web.api.weixin
# import nmp_web.api.api_test
