# coding=utf-8
from nmp_web import app
from flask import render_template


@app.route('/robots.txt')
def get_robots_txt_file():
    return render_template("robots.txt")


@app.route('/<no_static:owner>')
def get_owner_page(owner):
    return render_template("app/operation_system_app_index.html")


@app.route('/<no_static:owner>/<repo>')
@app.route('/<no_static:owner>/<repo>/')
@app.route('/<no_static:owner>/<repo>/status/head/')
def get_owner_repo_page(owner, repo):
    return render_template("app/operation_system_app_index.html")


@app.route('/<no_static:owner>/<repo>/status/head/<path:sms_path>', methods=['GET'])
def get_sms_status_page_by_path(owner, repo, sms_path):
    return render_template("app/operation_system_app_index.html")


@app.route('/<no_static:owner>/<repo>/aborted_tasks/<int:aborted_task_id>', methods=['GET'])
def get_sms_aborted_tasks_page(aborted_task_id, owner, repo):
    return render_template("app/operation_system_app_index.html")


@app.route('/<no_static:owner>/<repo>/task_check/unfit_nodes/<int:unfit_nodes_id>', methods=['GET'])
def get_sms_unfit_nodes_page(unfit_nodes_id, owner, repo):
    return render_template("app/operation_system_app_index.html")
