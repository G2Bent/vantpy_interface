#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from flask import json

from common import config,read_excel,write_excel
from common.http_service import HTTP
from openpyxl.styles import colors

#拼接URL，path参数是域名后面的虚拟目录部分
def get_url(path):
    return ''.join([config.base_url,path])

#封装requests请求方法，方法参数为：请求方式，接口URL，请求参数
def get_response(method,url,**DataALL):
    if method == 'get':
        resp = HTTP().get(url,**DataALL)
    elif method == 'put':
        resp = HTTP().put(url,**DataALL)
    elif method == 'post':
        resp = HTTP().post(url,**DataALL)
    elif method == 'delete':
        resp = HTTP().delete(url,**DataALL)
    else:
        return 'no the method'
    resp.encoding = 'UTF-8'
    return resp

#封装requests请求方法，请求参数testdata数据是从Excel表读取
def get_excel_response(testdata):
    method = testdata["method"]#请求方式
    url = testdata["url"]#请求url

    #url后面的params参数
    try:
        params = eval(testdata["params"])
    except:
        params = None

    #请求头部headers
    try:
        headers = eval(testdata["headers"])
    except:
        headers = None

    #post请求body内容
    try:
        bodydata = eval(testdata["body"])
        #可在这里实现excel的body里面耨个字段动态赋值，实现接口参数的关联，如token
        if 'accessToken' in testdata['body']:
            bodydata['accessToken'] = config.accessToken
    except:
        bodydata = {}


    #post请求body类型，判断传data数据还是json
    type = testdata["type"]
    if type == 'data':
        body = bodydata
    elif type == 'json':
        body = json.dumps(bodydata)
    else:
        body = json.dumps(bodydata)

    #发起网络请求，并返回数据
    try:
        r = requests.request(method = method,
                             url = url,
                             params = params,
                             headers = headers,
                             data = body)
        r.encoding = 'UTF-8'
        return r
    except Exception as msg:
        return msg

#这个是二次封装excel表数据，返回的data是列表类型，列表中子元素是字典类型
def get_excel_data(file_name,sheet_name):
    #filename是文件名（要带后缀），sheetName是表名
    sheet = read_excel.ReadExcel(config.test_data_path+file_name,sheet_name)
    data = sheet.get_dict_data()
    return data

#这个是二次封装Excel表数据，fileName是文件名，sheetName是表名，r是网络请求结果
def write_to_excel(file_name,sheet_name,test_data,r):
    #这里的文件夹路径要修改为你的
    write_excel.copy_excel(config.test_data_path+file_name) #拷贝一份测试数据
    wt = write_excel.WriteExcel(config.test_data_path+file_name,sheet_name)
    row = test_data.get('rowNum')
    color = colors.BLACK
    try:
        if test_data.get('isCheckStatusCode'):
            if str(r.status_code) == test_data.get('checkpoint'):
                wt.write(row,12,"pass",color)#测试结果为pass
            else:
                color = colors.RED
                wt.write(row,12,"fail",color) #测试结果为fail
        else:
            if test_data.get("checkpoint") =='':
                wt.write(row,12,'checkpoint为空',color.RED) #没有设置检查点得值
            elif test_data.get("checkpoint") in r.text:
                wt.write(row,12,"pass",color) #测试结果pass
            else:
                color = colors.RED
                wt.write(row,12,"fail",color) #测试结果为fail

        wt.write(row,10,str(r.status_code),color) #写入返回状态码statuscode,第8列
        wt.write(row,11,str(r.elapsed.total_seconds()),color) #耗时
        wt.write(row,13,r.text,color) #响应内容
        wt.write(row,14,"") #异常置空
        wt.wb.close()
    except Exception as e:
        color = colors.RED
        wt.write(row,10,"")
        wt.write(row,11,"")
        wt.write(row,12,"fail",color)
        wt.write(row,13,"")
        wt.write(row,14,str(r),color)
        wt.wb.close()
    return wt