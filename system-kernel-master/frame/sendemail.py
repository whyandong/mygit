# -*- coding: UTF-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import logging
import datetime
import base64
from frame import getLoginfo


def sendEmail():
    '''
    发送email
    '''
    username = 'xiaohaiyan@uniontech.com'
    m = 'eGh5QDIwMjAwNw=='
    password = base64.b64decode(m).decode('utf-8')
    sender = 'xiaohaiyan@uniontech.com'
    receiver = 'xiaohaiyan@uniontech.com'
    html_file = getLoginfo.getLastestHtml()
    log_file = getLoginfo.getLastestLog()
    content = getLoginfo.get_content()

    today = datetime.date.today()

    subject = 'dbus自动化测试报告 {}--本邮件自动发送，无需回复！'.format(today)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ";".join(receiver)

    # 编写html正文
    text = MIMEText(content, 'html', 'utf-8')
    text['Subject'] = Header('dbus_autotest_report', 'utf-8')
    msg.attach(text)

    # 构造log附件
    sendfile = open(r'{}'.format(log_file), 'rb').read()
    text_att = MIMEText(sendfile, 'base64', 'utf-8')
    text_att["Content-Type"] = 'application/octet-stream'
    text_att.add_header('Content-Disposition', 'attachment', filename='测试执行日志.txt')
    msg.attach(text_att)

    # 构造HTML附件
    sendHTMLfile = open(r'{}'.format(html_file), 'rb').read()
    HTMLfile = MIMEText(sendHTMLfile, 'base64', 'utf-8')
    HTMLfile["Content-Type"] = 'application/octet-stream'
    HTMLfile.add_header('Content-Disposition', 'attachment', filename='测试报告.html')
    msg.attach(HTMLfile)

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.uniontech.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

    logging.info("邮件发送完毕，请查收！")


if __name__ == '__main__':
    sendEmail()
