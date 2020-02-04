#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 张旭
# @Email   : zhangxu3486432@gmail.com
# @Blog    : https://zhangxu3486432.github.io
# @FileName: login.py
# @Time    : 2020/1/16

import time
from http import cookiejar
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from matplotlib import image
from matplotlib import pyplot

from settings import USERNAME, PASSWORD
from utils import logger


def login(session, name, pwd, code):
    """
    登陆 sep
    :return:
    """
    data = {
        'userName': name,
        'pwd': pwd,
        'certCode': code,
        'sb': 'sb'
    }
    resp = session.post(url='http://sep.ucas.ac.cn/slogin', data=data)
    text = resp.content.decode('utf-8')

    soup = BeautifulSoup(text, 'lxml')
    appform = soup.find(id="appform")
    if appform is not None:
        logger.error('验证码错误')
        raise PermissionError('验证码错误')
    session.cookies.save('sep.cookie')


def verification_code(session):
    params = {
        'code': int(time.time() * 1000)
    }
    resp = session.get(url='http://sep.ucas.ac.cn/changePic', params=params)
    img = image.imread(BytesIO(resp.content), 'jpg')
    pyplot.imshow(img)
    pyplot.imsave('verification.png', img)

    code = input('please input the code:')

    return code


if __name__ == '__main__':
    session = requests.Session()
    session.cookies = cookiejar.LWPCookieJar()
    code = verification_code(session)
    login(session, USERNAME, PASSWORD, code)
