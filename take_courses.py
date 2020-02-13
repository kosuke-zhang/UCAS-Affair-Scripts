#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 张旭
# @Email   : zhangxu3486432@gmail.com
# @Blog    : https://zhangxu3486432.github.io
# @FileName: take_courses.py
# @Time    : 2020/1/14

import re
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup

import settings
from utils import logger, send_email, identification


def take_courses(session, colleges, courses):
    colleges_dict = {}

    p_course_select = re.compile('"(\/courseManage\/selectCourse\?s=.*?)"')

    resp = session.get('http://jwxk.ucas.ac.cn/courseManage/main')

    soup = BeautifulSoup(resp.text, 'lxml')
    colleges_all = soup.find_all(name='label', attrs={'for': re.compile('^id_.*?')})

    p_college_id = re.compile('^id_(.*)')

    for college in colleges_all:
        college_id = p_college_id.search(college.attrs['for']).groups()[0]
        college_name = college.string
        colleges_dict[college_name] = college_id
    url_course_select = p_course_select.search(resp.text).groups()[0]
    url_course_select = 'http://jwxk.ucas.ac.cn{0}'.format(url_course_select)

    requests_count = 0
    data = [('sb', 0)]

    for college in colleges:
        college_id = colleges_dict.get(college, None)
        if college_id is not None:
            data.append(('deptIds', college_id))

    resp = session.post(url=url_course_select, data=data)

    soup = BeautifulSoup(resp.text, 'lxml')

    sids = []
    for course in courses:
        course = soup.find(text=course)
        if course is not None:
            value = course.parent.parent.parent.find(name='input', attrs={'name': 'sids'}).attrs['value']
            sids.append(value)
        else:
            logger.error('课程不存在：{0}'.format(course))

    p_save_course = re.compile('"(\/courseManage\/saveCourse\?s=.*?)"')

    url_save_course = p_save_course.search(resp.text).groups()[0]
    url_save_course = 'http://jwxk.ucas.ac.cn{0}'.format(url_save_course)

    while True:
        try:
            for value in sids:
                requests_count += 1
                resp = session.post(url_save_course, data=data[1:] + [('sids', value)])
                soup = BeautifulSoup(resp.text, 'lxml')
                sucess = soup.find(id='loginSuccess')
                error = soup.find(id='loginError')

                if sucess is not None and sucess.string is not None:
                    sids.remove(value)
                    sucess_info = sucess.string
                    logger.info(sucess_info)
                    send_email(sucess_info)

                if error is not None and error.string is not None:
                    error_info = error.string
                    if error_info == '你的会话已失效或身份已改变，请重新登录':
                        session = identification(session)
                        take_courses(session, colleges, courses)
                    if '时间冲突' in error_info:
                        sids.remove(value)
                    logger.info(error_info)
                time.sleep(settings.TAKE_COURSES_DELAY)

                if requests_count % 100 == 0:
                    # 为了防止域 sep.ucas.ac.cn 的 Cookie 过期，需要每隔一段时间对 domain 进行请求
                    session.get('http://sep.ucas.ac.cn/appStore')
                    session.cookies.save('sep.cookie')
                    logger.info('已经发送{0}次请求'.format(requests_count))

            if len(sids) == 0:
                logger.info('done')
                send_email('done')
                exit(0)

        except Exception as e:
            logger.error(e.args[0])


if __name__ == '__main__':
    session = requests.session()
    session.cookies = cookiejar.LWPCookieJar()
    session.cookies.load('sep.cookie')

    colleges = set(settings.COLLEGES)
    courses = set(settings.COURSES)
    session = identification(session)
    take_courses(session, colleges, courses)
