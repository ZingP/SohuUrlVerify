#! /usr/bin/env python3
"""
执行文件
"""
import os
import platform
import sys

if platform.system() == 'Windows':
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(BASE_DIR)

from core import main

if __name__ == "__main__":
    main.main()




