#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
import time

import os
from report.Runner import HTMLTestRunner3

def get_report(file):
    # dir指报告所在目录，listdir()方法是获取dir目录下所有文件和文件夹的列表
    lists = os.listdir(file)
    # 对列表进行排序，以创建时间顺序排序
    lists.sort(key=lambda fn: os.path.getatime(file + "\\" + fn))
    # 获取列表最后一个元素，即最新的HTML测试报告，再和目录dir拼接得到测试报告文件的路径
    file_name = os.path.join(file, lists[-1])
    # 返回获取到的测试报告文件的路径
    return file_name

if __name__=="__main__":
    #测试用例所在文件夹
    test_dir = './test_case'
    #自动识别用例，得到测试套件对象
    discover = unittest.defaultTestLoader.discover(test_dir,pattern = '*_test.py')
    # 设置时间的格式
    now_time = time.strftime('%Y-%m-%d %H-%M-%S')
    # 在目录demo_report下创建一个.html格式的文件，以当前时间命名
    filename = './report/' + now_time + '_test_result.html'
    # 以“wb”方式打开文件，如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    fp = open(filename, 'wb')
    # 调用写好的HTMLTestRunner指定生成报告的文件、标题和副标题
    runner = HTMLTestRunner3.HTMLTestRunner(stream=fp,
                                           title='Test Report',
                                           description='这是测试demo的测试报告：')
    # 执行测试用例集并生成报告
    runner.run(discover)
    # 关闭文件流
    fp.close()