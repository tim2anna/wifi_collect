# -*- coding: utf-8 -*-
DEBUG = True

SECRET_KEY = 'public'

SESSION_COOKIE_NAME = 'wifi_collect'

oracle_username = "opti"

oracle_pwd = "opti"

oracle_tnsname = "@ORCL_192.168.100.71" #oracle\ora92\network\admin\tnsnames.ora

SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://opti:opti@192.168.100.71:1521/orcl'

SQLALCHEMY_POOL_SIZE = 5

SQLALCHEMY_POOL_TIMEOUT = 10

SQLALCHEMY_ECHO = True

