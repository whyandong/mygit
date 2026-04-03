# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.getcwd())
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from public.log import LOG
from public import email_html


def load_emil_setting():
    """
    从配置文件中加载获取email的相关信息
    """
    import yaml
    data_file = open(os.path.join(os.getcwd(), "config/email.yaml"), "r")
    datas = yaml.load(data_file, Loader=yaml.FullLoader)
    data_file.close()
    return datas['from-email'], datas['password'], datas['to-email']


def sendemail(report_name_path, report_name, testCaseFilPath,
              testCaseFileName):
    """
    发送邮件
    """
    try:
        from_addr, password, mail_to = load_emil_setting()
        msg = MIMEMultipart()
        msg['Subject'] = '自动化测试报告'
        msg['From'] = '自动化测试平台'
        msg['To'] = mail_to
        msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        #发送测试报告
        atttestreport = MIMEText(
            open(r'%s' % report_name_path, 'rb').read(), 'base64', 'utf-8')
        atttestreport["Content-Type"] = 'application/octet-stream'
        # atttestreport["Content-Disposition"] = 'attachment; filename="%s"' % report_name
        # 解决附件文件名为中文的问题
        atttestreport.add_header("Content-Disposition",
                                 "attachment",
                                 filename=("gbk", "", report_name))

        #发送用例执行结果
        attcase = MIMEText(
            open(r'%s' % testCaseFilPath, 'rb').read(), 'base64', 'utf-8')
        attcase["Content-Type"] = 'application/octet-stream'
        attcase[
            "Content-Disposition"] = 'attachment; filename="%s"' % testCaseFileName

        txt = MIMEText(email_html.send_mail_excel_result(), 'html', 'utf-8')

        msg.attach(txt)
        msg.attach(atttestreport)
        msg.attach(attcase)

        server = smtplib.SMTP_SSL("smtp.163.com", 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, mail_to.split(','), msg.as_string())
        server.close()
    except Exception as e:
        LOG.error("邮件发送失败,失败原因是%s" % e)


if __name__ == '__main__':
    reportNamePath = os.path.join(os.getcwd(),
                                  'report/report_2023-05-26-14-00.html')
    reportName = '自动化测试报告2023-05-26-14-00.html'

    testCaseFilPath = os.path.join(os.getcwd(), 'casefile/case.xls')
    testCaseFileName = 'case.xls'
    sendemail(reportNamePath, reportName, testCaseFilPath, testCaseFileName)
