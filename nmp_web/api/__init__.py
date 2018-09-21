# coding=utf-8
from flask import Blueprint

api_app = Blueprint('api_app', __name__, template_folder='template')

import nmp_web.api.api_hpc
import nmp_web.api.api_sms
import nmp_web.api.api_weixin
import nmp_web.api.api_test
