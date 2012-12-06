#!/usr/bin/env python
# coding: utf-8
"""
    WiFi免费客户端采集 Web Server
    功能：获取手机客户端POST的数据，处理存入数据库
"""
import os
from datetime import datetime, timedelta, date
from flask import Flask, request, current_app
import simplejson as json
from collect.models import db, AssocTest,EnvTest, AuthTest, FtpTest, HttpTest, PingTest, RoamTest, StaInfo


app = Flask(__name__)
app.config.from_pyfile('settings.py')
db.init_app(app)
db.app = app

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
    attr_dict = json.loads(json.dumps(request.form))
    if name in ["assoc_test","env_test","auth_test","ftp_test","http_test","ping_test","roam_test","sta_info"]:  # 数据保存文件
        now = datetime.now()
        filename = name+now.strftime('-%Y-%m-%d-%H') + '.txt'
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename), 'a') as file:
            name_cn, model = view_config.get(name)
            record = [attr_dict.get(column.name,str(column.default.arg) if column.default else '') for column in model.__table__.columns]
            file.write('|'.join(record) + '\n')
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
def load_files():
    now = datetime.now() - timedelta(hours=1)
    from settings import oracle_username,oracle_pwd,oracle_tnsname
    for name in view_config.keys():
        ctl_file = create_ctl_file(name)
        if ctl_file:
            #执行sqlldr user_name/password@tnsname control=控制文件名
            sqlldr_cmd = "sqlldr %s/%s%s control=%s" % (oracle_username,oracle_pwd, oracle_tnsname,ctl_file)
            os.system(sqlldr_cmd)
            # 调用存储
    return "success"

def create_ctl_file(name):
    now = datetime.now() - timedelta(hours=1)
    filename = name+now.strftime('-%Y-%m-%d-%H') + '.txt'
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename)
    if not os.path.exists(data_file): return
    name_cn, model = view_config.get(name)
    columns = [(d.name,d.type.python_type) for d in model.__table__.columns]
    fields = []
    for col_name, col_type in columns:
        field = col_name
        if col_type is datetime:
            field += " Date 'yyyy-mm-dd HH24:mi:ss'"
        elif col_type is date:
            field += " Date 'yyyy-mm-dd'"
        fields.append(field)

    ctl_content = '''OPTIONS(ERRORS=100000)
        Load DATA
        INFILE '%(file_name)s'
        TRUNCATE INTO TABLE %(table_name)s
        Fields terminated by "|"
        TRAILING NULLCOLS
        (%(fields)s)
    ''' % {
        "table_name": model.__tablename__,
        "fields": ", ".join(fields),
        "file_name": data_file
    }
    ctl_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", name+".ctl")
    with open(ctl_file,'wb') as f:
        f.write(ctl_content)
    return ctl_file

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

