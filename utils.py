#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from settings import SEND_EMAIL, SEND_EMAIL_PWD, RECEIVE_EMAIL

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d: - %(levelname)s: - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# 使用 FileHandler 输出到文件
# fh = logging.FileHandler('take-courses.txt', mode='w')
# fh.setLevel(logging.ERROR)
# fh.setFormatter(formatter)

# 使用 StreamHandler 输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

# 添加两个 Handler
# logger.addHandler(fh)
logger.addHandler(ch)


def email_set():
    if SEND_EMAIL and SEND_EMAIL_PWD and RECEIVE_EMAIL:
        return True
    return False


def send_email(str, file_path=None):
    if not email_set():
        return False

    try:
        msg = MIMEMultipart()
        part = MIMEText(str, 'plain', 'utf-8')
        msg.attach(part)

        if file_path:
            part = MIMEApplication(open('./static/email_file/' + file_path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', file_path))
            msg.attach(part)

        msg['From'] = formataddr((SEND_EMAIL, SEND_EMAIL))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr((RECEIVE_EMAIL, RECEIVE_EMAIL))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "UCAS-Affair-Scripts notification"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(SEND_EMAIL, SEND_EMAIL_PWD)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(SEND_EMAIL, [RECEIVE_EMAIL, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        return True
    except Exception:
        return False


def identification(session):
    logger.info('选课系统会话失效，正在重新认证。（如果您需要使用网页端，请先暂停此脚本，否则此脚本会不断抢夺选课系统的认证）')
    p_course_manage = re.compile('(http:\/\/jwxk\.ucas\.ac\.cn\/login\?Identity=.*?&roleId=821)')

    resp = session.get('http://sep.ucas.ac.cn/portal/site/226/821')
    url_course_manage = p_course_manage.search(resp.text).groups()[0]

    session.get(url_course_manage)
    session.cookies.save('sep.cookie')

    return session
