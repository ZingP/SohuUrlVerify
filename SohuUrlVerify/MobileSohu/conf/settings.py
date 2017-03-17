#! /usr/bin/env python3
"""
配置文件
"""
from bin.run import BASE_DIR
import os

# 初始URL
BASE_URL = 'http://m.sohu.com/'

# 错误日志路径
ERROR_LOG = os.path.join(BASE_DIR, 'log', 'error.log')

# 线程池数量
THREAD_NUM = 300


