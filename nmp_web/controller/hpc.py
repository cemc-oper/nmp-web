# coding=utf-8
from nmp_web import app
from flask import render_template


@app.route('/hpc/nwp_xp/disk/usage', methods=['GET'])
def get_hpc_disk_usage():
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/info/disk/space', methods=['GET'])
def get_hpc_disk_space():
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/<user>/loadleveler/status', methods=['GET'])
@app.route('/hpc/<user>/loadleveler/status/', methods=['GET'])
def get_hpc_loadleveler_status(user):
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/<user>/loadleveler/status/job_detail/<job_id>', methods=['GET'])
@app.route('/hpc/<user>/loadleveler/status/job_detail/<job_id>/', methods=['GET'])
def get_hpc_loadleveler_status_job_detail(user, job_id):
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/<user>/loadleveler/abnormal_jobs/<abnormal_jobs_id>', methods=['GET'])
@app.route('/hpc/<user>/loadleveler/abnormal_jobs/<abnormal_jobs_id>/', methods=['GET'])
def get_hpc_loadleveler_abnormal_jobs(user, abnormal_jobs_id):
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/<user>/loadleveler/abnormal_jobs/<abnormal_jobs_id>/job_detail/<job_id>', methods=['GET'])
@app.route('/hpc/<user>/loadleveler/abnormal_jobs/<abnormal_jobs_id>/job_detail/<job_id>/', methods=['GET'])
def get_hpc_loadleveler_abnormal_job_detail(user, abnormal_jobs_id, job_id):
    return render_template('app/hpc_app_index.html')
