#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

#主机
base_url = 'https://httpbin.org'
#获取本文件的上上级路径（这里是获取项目路径）
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))

test_case_path = project_path+'//test_case//'
test_data_path = project_path+'//test_data//'
report_path = project_path+'//report//'
logs_path = project_path+'//logs//'
