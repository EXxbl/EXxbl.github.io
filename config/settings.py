import os
import datetime


# 根路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 日志路径
logpath = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(logpath):
    os.mkdir(logpath)

today = str(datetime.datetime.today())[:10].replace('-', '')
data_path = os.path.join(BASE_DIR, 'logs\\' + today)
if not os.path.exists(data_path):
    os.mkdir(data_path)


# js路劲
jspath = os.path.join(BASE_DIR, 'js')
