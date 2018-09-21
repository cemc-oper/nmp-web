# coding=utf-8
from flask import render_template, request, redirect, current_app

from nmp_web.common.user import get_user_info


@current_app.route('/')
@current_app.route('/about')
def get_index_page():
    code = request.args.get('code', None)
    get_user_info(code)

    return render_template("app/welcome_app_index.html")


@current_app.route('/login')
def login():
    return redirect(
        "https://open.weixin.qq.com/connect/oauth2/authorize?"
        "appid={app_id}&redirect_uri={redirect_uri}&"
        "response_type=code&scope=SCOPE&state=STATE#wechat_redirect".format(
            app_id=current_app.config['NWPC_MONITOR_WEB_CONFIG']['weixin_app']['token']['corp_id'],
            redirect_uri='https%3A%2F%2Fwww.nwpcmonitor.cc%2Fabout'
        ))
