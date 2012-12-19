# coding: utf-8
import sys
import os
sys.path.insert(0, os.getcwd())

CELERY_IMPORTS = (
    "webapp",
    )

BROKER_URL = "sqla+sqlite:///conf//celery.db"

## Using the database to store results
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = u"sqlite:///conf//celery.db"

# 计划任务
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'runs-every-1-hour': {
        'task': 'webapp.load_files',
        'schedule': timedelta(seconds=10)   #minutes=15
    },
}
