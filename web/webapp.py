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

procedure_config = [
    ('sta_info', 8),
    ('env_test', 1),
    ('assoc_test', 2),
    ('roam_test', 3),
    ('auth_test', 4),
    ('ping_test', 5),
    ('ftp_test', 6),
    ('http_test', 7),
]

def get_default(default):
    if callable(default.arg):
        return default.arg(0)
    else:
        return default.arg

time_fileds = {
    "assoc_test": [
        ('assocsucc_time','assoc_req_start_time','assoc_delay'),
        ('dhcp_req_succ_time','dhcp_req_start_time','dhcp_delay'),
    ],
    "auth_test": [
        ('portal_succ_time','portal_req_time','portal_delay'),
        ('auth_succ_time','auth_req_time','auth_delay'),
    ],
    "http_test": [
        ('http_req_end_time','http_req_start_time','http_delay'),
    ],
}

# 处理时延
def get_delay(attr_dict, time_fileds):
    try:
        format_str = '%Y-%m-%d %H:%M:%S:%f'
        for succ_time_field, start_time_field, delay_field in time_fileds:
            succ_time = attr_dict.get(succ_time_field)
            start_time = attr_dict.get(start_time_field)
            if succ_time and not start_time:
                attr_dict[delay_field] = '0'
                attr_dict[start_time_field] = succ_time
            elif not succ_time and start_time:
                attr_dict[delay_field] = '0'
                attr_dict[succ_time_field] = start_time
            elif succ_time and start_time:
                start_time = datetime.strptime(start_time,format_str)
                succ_time = datetime.strptime(succ_time,format_str)
                if start_time > succ_time:   #处理成功时间小于开始时间的清空
                    attr_dict[delay_field] = '0'
                    attr_dict[start_time_field] = attr_dict[succ_time_field]
                else:
                    delay = succ_time - start_time
                    attr_dict[delay_field] = str(int(1000*delay.total_seconds()))
            else:
                return
    except :
        pass
    return attr_dict

@app.route('/collect/<name>/', methods=['GET', 'POST'])
def collect(name):
    if name not in view_config: return "fail"
    now = datetime.now()
    filename = name+now.strftime('-%Y-%m-%d-%H') + '.txt'
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename), 'a') as file:
        name_cn, model = view_config.get(name)
        data = request.form.get(name)
        if data:
            data_list = json.loads(data)
            for attr_dict in data_list:
                if name in ["assoc_test","auth_test", "http_test"]:
                    attr_dict = get_delay(attr_dict,time_fileds[name])     # 处理时延
                    if not attr_dict: return "fail"
                record = []
                for column in model.__table__.columns:
                    value = attr_dict.get(column.name,str(get_default(column.default)) if column.default else '')
                    if column.name in ['sta_mac','ssid_mac','current_ssid_mac']:
                        value = value.upper()
                    record.append(value)
                file.write('|'.join(record) + '\n')
        else:
            attr_dict = json.loads(json.dumps(request.form))
            if name in ["assoc_test","auth_test","http_test"]:
                attr_dict = get_delay(attr_dict,time_fileds[name])     # 处理时延
                if not attr_dict: return "fail"
            record = []
            for column in model.__table__.columns:
                value = attr_dict.get(column.name,str(get_default(column.default)) if column.default else '')
                if column.name in ['sta_mac','ssid_mac','current_ssid_mac']:
                    value = value.upper()
                record.append(value)
            file.write('|'.join(record) + '\n')
    return "success"

from celery.task import task

@task()
def load_files():
    now = datetime.now() - timedelta(hours=1)
    from settings import oracle_username,oracle_pwd,oracle_tnsname
    procedure_name = []
    for name in view_config.keys():
        ctl_file = create_ctl_file(name)
        if ctl_file:
            #执行sqlldr user_name/password@tnsname control=控制文件名
            sqlldr_cmd = "sqlldr %s/%s%s control=%s log=log/%s.log" % (oracle_username,oracle_pwd, oracle_tnsname,ctl_file[0],name)
            os.system(sqlldr_cmd)
            os.system("mv %s %s.old" % (ctl_file[1],ctl_file[1]))
            procedure_name.append(name)
    for name, p_type in procedure_config:
        param_values = [date.today(), str(now.hour), p_type,]
        if name in procedure_name or name=='sta_info': call_procedure("wlan_deal_perception_task",param_values)
    return "success"

def call_procedure(procedure_name, param_values):
    import cx_Oracle
    from settings import oracle_dsn, oracle_username, oracle_pwd
    conn = cx_Oracle.connect(oracle_username, oracle_pwd, oracle_dsn)
    cursor = conn.cursor()
    oracle_cursor = cursor.var(cx_Oracle.NUMBER)
    param_values.append(oracle_cursor)
    res = cursor.callproc(procedure_name, param_values)
    cursor.close()
    conn.close()
    return res[-1]

def create_ctl_file(name):
    now = datetime.now() - timedelta(hours=1)
    filename = name+now.strftime('-%Y-%m-%d-%H') + '.txt'
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file", filename)
    if not os.path.exists(data_file): return
    name_cn, model = view_config.get(name)
    columns = [(d.name,d.type) for d in model.__table__.columns]
    fields = []
    for col_name, col_type in columns:
        field = col_name
        if isinstance(col_type, db.TIMESTAMP):
            field += " timestamp 'yyyy-mm-dd HH24:mi:ss:ff6'"
        elif isinstance(col_type, db.DateTime):
            field += " Date 'yyyy-mm-dd HH24:mi:ss'"
        elif isinstance(col_type, db.Date):
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
    return ctl_file,data_file

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)

