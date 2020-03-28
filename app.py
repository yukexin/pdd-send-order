# -*- coding: utf-8 -*-
import requests
import json
import os
import time
import hashlib
import common
from flask import Flask, request, url_for, send_from_directory, render_template, redirect
from utils import param, db, excel
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['xls'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

access_token = ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    access_token = db.find()
    if access_token == 'empty':
        return redirect(
            'https://mai.pinduoduo.com/h5-login.html?response_type=code&client_id=86b52cf3146d42dfb4ca0ff994006db0&redirect_uri=http://boss-vip.utools.club/access_token&&state=1212&view=h5')
    else:
        return render_template('index.html', auth_title='已授权')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            excel.read_excel_send(filename)
            return '表格上传成功，发送中'
    return render_template('index.html', auth_title='授权')


@app.route('/access_token', methods=['GET', 'POST'])
def access_token():
    # 授权获取code
    code = request.values['code']
    adata = {
        'code': code,
    }
    response = requests.post('https://open-api.pinduoduo.com/oauth/token',
                             headers=common.aheaders,
                             data=json.dumps(param.data_param(adata)))
    response_json = response.json()
    print(response_json)
    access_token = response_json['access_token']
    print(access_token)
    db.insert_one({
        'access_token': access_token,
        'timestamp': str(int(time.time()))
    })
    return render_template('index.html', auth_title='已授权')


@app.route('/get_express', methods=['GET', 'POST'])
def get_express():
    adata = {
        'type': 'pdd.logistics.companies.get',
        'client_id': common.client_id,
        'timestamp': str(int(time.time())),
    }

    response = requests.post(common.url,
                             headers=common.aheaders,
                             data=json.dumps(param.data_sign(adata)))
    return response.json()


if __name__ == '__main__':
    app.run()
