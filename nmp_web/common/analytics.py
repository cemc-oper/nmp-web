# coding=utf-8
import uuid
import requests

from nmp_web import app


REQUEST_POST_TIME_OUT = 20


def send_google_analytics_page_view(page_url):
    google_analytics_config = app.config['NWPC_MONITOR_WEB_CONFIG']['analytics']['google_analytics']
    if google_analytics_config['enable'] is True:
        print('send data to google analytics')
        post_data = {
            'v': google_analytics_config['version'],
            't': 'pageview',
            'tid': google_analytics_config['track_id'],
            'cid': str(uuid.uuid4()),
            'dh': google_analytics_config['document_host'],
            'dp': page_url
        }
        response = requests.post(google_analytics_config['url'], data=post_data, timeout=REQUEST_POST_TIME_OUT)
