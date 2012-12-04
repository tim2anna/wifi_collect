# -*- coding: utf-8 -*-
from web import webapp
import unittest
import random
from datetime import datetime
import time

mac_dict = {
    1: '08:18:1A:2F:67:04',
    2: '00:15:EB:F9:8C:57',
    3: '00:15:ED:F9:53:A9',
    4: '00:1E:73:D9:15:A3',
    5: '00:1E:73:D9:15:C2',
}

ip_dict = {
    1: '136.17.105.79',
    2: '136.17.103.137',
    3: '136.17.103.173',
    4: '136.17.103.172',
    5: '136.17.105.228',
}

encrypt_dict = {
    1: 'WEP',
    2: 'WPA',
    3: 'WPA2',
}

radio_model_dict = {
    1: '11a',
    2: '11b',
    3: 'g',
}

wireless_auth_model_dict = {
    1: 'none',
    2: 'opensystem',
    3: 'sharekey',
}
class CollectTestCase(unittest.TestCase):
    def setUp(self):
        self.app = webapp.app.test_client()

    def collect(self, name, attr_dict):
        return self.app.post('/collect/'+name+'/', data=attr_dict)

    def env_test(self, sta_mac):
        name = "env_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["sampletime"] = time.time()
        attr_dict["ssid"] = "test_ssid_"+str(random.randint(100,200))
        attr_dict["frequency"] = random.randint(1000,10000)
        attr_dict["ssid_mac"] = sta_mac
        attr_dict["sta_down_rssi"] = random.randint(1000,10000)
        attr_dict["encrypt"] = encrypt_dict.get(random.randint(1,3))
        attr_dict["work_model"] = 'Infrastructure'
        attr_dict["radio_model"] = radio_model_dict.get(random.randint(1,3))
        attr_dict["wireless_auth_model"] = wireless_auth_model_dict.get(random.randint(1,3))

        self.collect(name, attr_dict)

    def assoc_test(self, sta_mac):
        name = "assoc_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["assoc_req_start_time"] = time.time()
        attr_dict["dhcp_req_start_time"] = time.time()
        attr_dict["frequency"] = random.randint(1000,10000)
        attr_dict["assoc_req_ssid"] = "test_ssid_"+str(random.randint(100,200))
        attr_dict["assoc_status"] = random.randint(0,1)
        attr_dict["ap_txrates"] = random.randint(12,60)
        attr_dict["ssid_mac"] = mac_dict.get(random.randint(1,5))
        attr_dict["sta_ip"] = ip_dict.get(random.randint(1,5))
        attr_dict["sta_down_rssi"] = random.randint(1000,10000)
        attr_dict["dhch_req_status"] = random.randint(0,1)
        attr_dict["encrypt"] = encrypt_dict.get(random.randint(1,3))
        attr_dict["work_model"] = 'Infrastructure'
        attr_dict["radio_model"] = radio_model_dict.get(random.randint(1,3))
        attr_dict["wireless_auth_model"] = wireless_auth_model_dict.get(random.randint(1,3))
        attr_dict["assocsucc_time"] = time.time()
        attr_dict["dhcp_req_succ_time"] = time.time()

        self.collect(name, attr_dict)

    def auth_test(self, sta_mac):
        name = "auth_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["auth_req_time"] = time.time()
        attr_dict["login"] = "test_login_"+str(random.randint(100,200))
        attr_dict["auth_status"] = random.randint(0,1)
        attr_dict["auth_succ_time"] = time.time()
        self.collect(name, attr_dict)

    def ftp_test(self, sta_mac):
        name = "ftp_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["up_down_url"] = "http://test.com/?trest_true"
        attr_dict["model"] = random.randint(1,2)
        attr_dict["up_down_file_size"] = random.randint(0,100)
        attr_dict["up_down_elapsed"] = random.randint(0,100)
        attr_dict["up_down_speed_max"] = random.randint(0,100)
        self.collect(name, attr_dict)

    def http_test(self, sta_mac):
        name = "http_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["http_req_start_time"] = time.time()
        attr_dict["http_url"] = "http://test.com/?trest_true"
        attr_dict["up_down_speed_max"] = random.randint(0,100)
        attr_dict["http_req_end_time"] = time.time()
        self.collect(name, attr_dict)

    def ping_test(self, sta_mac):
        name = "ping_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["ping_url"] = "http://test.com/?trest_true"
        attr_dict["ping_count"] = random.randint(1,200)
        attr_dict["pingok_count"] = random.randint(0,attr_dict["ping_count"])
        attr_dict["ping_delay_min"] = random.randint(0,10)
        attr_dict["ping_delay_max"] = random.randint(50,100)
        attr_dict["ping_delay_avg"] = random.randint(attr_dict["ping_delay_min"],attr_dict["ping_delay_max"])
        self.collect(name, attr_dict)

    def roam_test(self,sta_mac):
        name = "roam_test"
        attr_dict = {}
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().hour
        attr_dict["sta_mac"] = sta_mac
        attr_dict["roam_reassoc_req_time"] = time.time()
        attr_dict["roam_req_ap"] = "test_ap_"+str(random.randint(100,200))
        attr_dict["ap_txrates"] = random.randint(100,1000)
        attr_dict["channel"] = "test_channel"+str(random.randint(0,100))
        attr_dict["ssid_mac"] = mac_dict.get(random.randint(1,5))
        attr_dict["roam_assoc_status"] = random.randint(0,1)
        attr_dict["sta_down_rssi"] = random.randint(1000,10000)
        attr_dict["encrypt"] = encrypt_dict.get(random.randint(1,3))
        attr_dict["work_model"] = 'Infrastructure'
        attr_dict["radio_model"] = radio_model_dict.get(random.randint(1,3))
        attr_dict["wireless_auth_model"] = wireless_auth_model_dict.get(random.randint(1,3))
        attr_dict["assocsucc_time"] = time.time()
        self.collect(name, attr_dict)

    def sta_info(self, sta_mac):
        name = "sta_info"
        attr_dict = {}
        attr_dict["regdate"] = time.time()
        attr_dict["sta_mac"] = sta_mac
        attr_dict["sta_status"] = random.randint(1,2)
        attr_dict["sta_kernel_ver"] = '2.6.35.7-overseas'
        attr_dict["sta_os"] = 'Linux'
        attr_dict["sta_type"] = 'M9'
        attr_dict["sta_vendor"] = 'Meizu'
        attr_dict["report_time"] = time.time()
        attr_dict["sampledate"] = time.time()
        attr_dict["samplehour"] = datetime.now().month
        self.collect(name, attr_dict)

    def test_total(self):
        for i in range(0,100):
            sta_mac = mac_dict.get(random.randint(1,5))
            self.sta_info(sta_mac)
            self.roam_test(sta_mac)
            self.ping_test(sta_mac)
            self.http_test(sta_mac)
            self.ftp_test(sta_mac)
            self.auth_test(sta_mac)
            self.env_test(sta_mac)
            self.assoc_test(sta_mac)


if __name__ == '__main__':
    unittest.main()