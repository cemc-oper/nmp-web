from flask import request, jsonify, json
import gzip
from nmp_web.api import api_app


@api_app.route("/test/gzip")
def gzip_hello_page():
    return "This page is used to test gzip on request body."


@api_app.route("/test/gzip/normal", methods=['POST'])
def get_normal_data():
    message = request.form['message']
    return jsonify({
        'status': 'ok'
    })


@api_app.route("/test/gzip/compress", methods=['POST'])
def get_gzip_data():
    content_encoding = request.headers.get('content-encoding', '').lower()
    gzipped_data = request.data

    if content_encoding == 'gzip':
        print('decompress gzip data')
        data_string = gzip.decompress(gzipped_data)
        data = json.loads(data_string.decode('utf-8'))
        message = data['message']
    return jsonify({
        'status': 'ok'
    })
