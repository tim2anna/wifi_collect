#!/usr/bin/env python
# coding: utf-8
"""
    WiFi免费客户端采集 Web Server
    功能：获取手机客户端POST的数据，处理存入数据库
"""
import os
from datetime import datetime, timedelta
from flask import Flask, request
import simplejson as json
from collect.models import db, AssocTest,EnvTest, AuthTest, FtpTest, HttpTest, PingTest, RoamTest, StaInfo


app = Flask(__name__)
app.config.from_pyfile('settings.py')
db.init_app(app)
db.app = app

app.config['file_status'] = 0

view_config = {
    'assoc_test': (u'关联测试', AssocTest),
    'env_test': (u'环境测试', EnvTest),
    'auth_test': (u'认证测试', AuthTest),
    'ftp_test': (u'FTP测试', FtpTest),
    'http_test': (u'HTTP测试', HttpTest),
    'ping_test': (u'PING测试', PingTest),
    'roam_test': (u'漫游测试', RoamTest),
    'sta_info': (u'终端信息', StaInfo),
}

@app.route('/collect/<name>/', methods=['GET', 'POST'])
def collect(name):
    if name not in view_config: return "fail"
    attr_dict = request.form
    if name in ["env_test","sta_info"]:  # 环境测试，数据保存文件，15分钟定时读取文件入库
        now = datetime.now()
        quarter = str(int(now.strftime('%M')) // 15)
        filename = name+now.strftime('-%Y-%m-%d-%H-') + quarter + '.txt'
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename), 'a') as file:
            file.write(json.dumps(attr_dict) + '\n')
        return "success"
    else:   # 其它直接存数据库
        name_cn, model = view_config[name]
        obj = model()
        obj = load_obj(obj, attr_dict)
        db.session.add(obj)
        db.session.commit()
        return "success"

from celery.task import task

@task()
def read_files():
    now = datetime.now() - timedelta(minutes=15)
    quarter = str(int(now.strftime('%M')) // 15)
    for name in view_config.keys():
        filename = name+now.strftime('-%Y-%m-%d-%H-') + quarter + '.txt'
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename)
        if not os.path.exists(file): continue
        with open(file,'rb') as f:
            for  line in  f.readlines():
                name_cn, model = view_config[name]
                obj = model()
                obj = load_obj(obj, json.loads(line))
                db.session.add(obj)
        #os.remove(file)
        db.session.commit()
    return "success"

# 将attr_dict加载到obj的属性中
def load_obj(obj, attr_dict):
    for attr_name, attr_value in attr_dict.items():
        if 'time' in attr_name or 'date' in attr_name:
            attr_value = datetime.utcfromtimestamp(float(attr_value))
        if hasattr(obj,attr_name):
            setattr(obj, attr_name, attr_value)
    return obj

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)

