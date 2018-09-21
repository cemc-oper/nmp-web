# coding=utf-8
from flask import current_app
from nmp_web.common.weixin import Auth

auth = Auth(current_app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']['token'])
weixin_access_token = auth.get_access_token_from_server()
