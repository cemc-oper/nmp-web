# coding=utf-8
from nmp_web import app
from nmp_web.common.weixin import Auth

auth = Auth(app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']['token'])
weixin_access_token = auth.get_access_token_from_server()
