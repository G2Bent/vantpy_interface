#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from common.log import Log
class HTTP(object):
    '网络请求封装'
    def __init__(self):
        self.log = Log('HTTP').get_logger()

    def get(self,url,**kwargs):
        params = kwargs.get('params')
        headers = kwargs.get('headers')
        cookies = kwargs.get('cookies')
        try:
            r = requests.get(url,params = params,headers=headers,cookies =cookies,timeout = 30)
            return r
        except Exception as e:
            self.log.error('get请求出错:%s'%e)

    def post(self,url,**kwargs):
        params = kwargs.get('params')
        headers = kwargs.get('headers')
        cookies = kwargs.get('cookies')
        data = kwargs.get('data')
        json = kwargs.get('json')
        try:
            r = requests.get(url, params=params, headers=headers, data= data,json=json,cookies=cookies, timeout=50)
            return r
        except Exception as e:
            self.log.error('post请求出错:%s' % e)