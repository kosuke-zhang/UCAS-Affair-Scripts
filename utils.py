#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from settings import SEND_EMAIL, SEND_EMAIL_PWD

logger = logging.getLogger(__name__)  # 不加名称设置root logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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


def send_email(str, email_receiver, file_path=None):
    ret = True
    try:
        msg = MIMEMultipart()
        part = MIMEText(str, 'plain', 'utf-8')
        msg.attach(part)

        if file_path:
            part = MIMEApplication(open('./static/email_file/' + file_path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', file_path))
            msg.attach(part)

        msg['From'] = formataddr((SEND_EMAIL, SEND_EMAIL))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr((email_receiver, email_receiver))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "成绩"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(SEND_EMAIL, SEND_EMAIL_PWD)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(SEND_EMAIL, [email_receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
    except Exception:
        ret = False
    return ret
