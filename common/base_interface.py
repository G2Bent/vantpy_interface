#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from flask import json

from common import config,read_excel,write_excel
from common.http_service import HTTP