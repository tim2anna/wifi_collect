# -*- coding: utf-8 -*-
'''
    SQLAlchemy Model
'''
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AssocTest(db.Model):
    '''
        关联测试
    '''
    __tablename__ = 'wlan_perception_assoc_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    assoc_req_ssid      = db.Column(db.String(50))      # 关联请求SSID
    ssid_mac            = db.Column(db.String(50))      # SSID MAC
    assoc_req_start_time= db.Column(db.TIMESTAMP)       # 关联请求开始时间
    assocsucc_time      = db.Column(db.TIMESTAMP)       # 关联成功时间
    assoc_status        = db.Column(db.Integer)         # 关联状态
    ap_txrates          = db.Column(db.Integer)         # 协商速率
    frequency           = db.Column(db.Integer)         # 频率
    sta_down_rssi       = db.Column(db.Integer)         # 下行信号强度
    encrypt             = db.Column(db.String(50))      # 加密方式
    work_model          = db.Column(db.String(50))      # 工作模式
    radio_model         = db.Column(db.String(50))      # 射频模式
    wireless_auth_model = db.Column(db.String(50))      # 无线鉴权模式
    dhcp_req_start_time = db.Column(db.TIMESTAMP)       # DHCP请求开始时间
    dhcp_req_succ_time  = db.Column(db.TIMESTAMP)       # DHCP获取成功时间
    dhcp_req_status     = db.Column(db.Integer)         # DHCP获取状态
    sta_ip              = db.Column(db.String(50))      # 终端IP地址
    channel             = db.Column(db.String(20))      # 信道
    assoc_delay         = db.Column(db.Integer)         # 关联时延
    dhcp_delay          = db.Column(db.Integer)         # DHCP时延


class AuthTest(db.Model):
    '''
        认证测试
    '''
    __tablename__ = 'wlan_perception_auth_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    login           = db.Column(db.String(100))      # 账号
    auth_req_time   = db.Column(db.TIMESTAMP)      # 认证请求时间
    auth_succ_time  = db.Column(db.TIMESTAMP)       # 认证成功时间
    auth_status     = db.Column(db.Integer)         # 认证状态


class EnvTest(db.Model):
    '''
        环境测试
    '''
    __tablename__ = 'wlan_perception_env_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    sampletime          = db.Column(db.DateTime)      # 时间
    ssid                = db.Column(db.String(100))    # SSID
    frequency           = db.Column(db.Integer)        # 频率
    ssid_mac            = db.Column(db.String(100))    # SSID MAC
    sta_down_rssi       = db.Column(db.Integer)        # 下行信号强度
    encrypt             = db.Column(db.String(50))     # 加密方式
    work_model          = db.Column(db.String(50))     # 工作模式
    radio_model         = db.Column(db.String(50))     # 射频模式
    wireless_auth_model = db.Column(db.String(50))     # 无线鉴权模式
    channel             = db.Column(db.String(20))      # 信道

class FtpTest(db.Model):
    '''
        FTP测试
    '''
    __tablename__ = 'wlan_perception_ftp_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    up_down_url     = db.Column(db.String(500))      # FTP上传下载URL
    model           = db.Column(db.Integer)      # 模式
    up_down_file_size  = db.Column(db.Integer)       # FTP上传下载文件大小
    up_down_elapsed = db.Column(db.Integer)          # 上传下载耗时
    up_down_speed_max = db.Column(db.Integer)        # FTP上传下载最大速率


class HttpTest(db.Model):
    '''
        HTTP测试
    '''
    __tablename__ = 'wlan_perception_http_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    http_url            = db.Column(db.String(500))      # HTTP访问URL
    http_req_start_time = db.Column(db.TIMESTAMP)      # HTTP请求开始时间
    http_req_end_time   = db.Column(db.TIMESTAMP)       # HTTP请求完成时间
    http_req_bytes      = db.Column(db.Integer)         # HTTP请求字节数


class PingTest(db.Model):
    '''
        PING测试
    '''
    __tablename__ = 'wlan_perception_ping_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    ping_url        = db.Column(db.String(500))      # PING访问URL
    ping_count      = db.Column(db.Integer)       # PING请求次数
    pingok_count    = db.Column(db.Integer)       # PING成功次数
    ping_delay_avg  = db.Column(db.Integer)       # PING平均时延
    ping_delay_min  = db.Column(db.Integer)       # PING最小时延
    ping_delay_max  = db.Column(db.Integer)       # PING最大时延


class RoamTest(db.Model):
    '''
        漫游测试
    '''
    __tablename__ = 'wlan_perception_roam_test'
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    sta_mac               = db.Column(db.String(50), primary_key=True)
    roam_req_ap           = db.Column(db.String(255))   # 漫游请求AP
    roam_reassoc_req_time = db.Column(db.TIMESTAMP)     # 漫游重关联请求开始时间
    assocsucc_time        = db.Column(db.TIMESTAMP)     # 关联成功时间
    roam_assoc_status     = db.Column(db.Integer)       # 漫游关联成功状态
    ap_txrates            = db.Column(db.Integer)       # 协商速率
    channel               = db.Column(db.String(20))    # 信道
    sta_down_rssid        = db.Column(db.Integer)       # 下行信号强度
    encrypt               = db.Column(db.String(50))    # 加密方式
    work_model            = db.Column(db.String(50))    # 工作模式
    radio_model           = db.Column(db.String(50))    # 射频模式
    wireless_auth_model   = db.Column(db.String(50))    # 无线鉴权模式


class StaInfo(db.Model):
    '''
        终端信息
    '''
    __tablename__ = 'wlan_perception_sta_info'
    sta_mac        = db.Column(db.String(100), primary_key=True)      # 终端MAC地址
    sta_vendor     = db.Column(db.String(100))       # 终端厂家
    sta_type       = db.Column(db.String(255))       # 终端型号
    sta_os         = db.Column(db.String(100))       # 终端操作系统
    sta_kernel_ver = db.Column(db.String(100))       # 终端内核版本
    regdate        = db.Column(db.DateTime, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))         # 注册时间
    report_time    = db.Column(db.DateTime, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))         # 上报时间
    sta_status     = db.Column(db.String(50), default='1')        # 终端M状态
    sampledate     = db.Column(db.Date, default=lambda: date.today().strftime('%Y-%m-%d'))
    samplehour     = db.Column(db.Integer, default=lambda: datetime.now().hour)
    ssid_mac       = db.Column(db.String(100))    # SSID MAC
