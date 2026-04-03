# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.getcwd())

import pandas as pd
from interface.oper_excel import sum_test_results
from datetime import datetime
import re


def Godsaycolor(filter_merge_data, html_text, idx_col):
    td_text = re.findall("<td>(.*?)</td>", html_text)
    for i in range(filter_merge_data.shape[0]):
        text = td_text[i * filter_merge_data.shape[1] + idx_col]
        html_text_fin = html_text.replace(
            '<td>' + text, '<td style="color: #de4040">' + text)
    return html_text_fin


def send_mail_excel_result():
    """
    邮件html内容
    """
    pd.set_option('display.max_colwidth', 10000)
    columns = ['测试模块', '用例总数', '通过总数', '失败总数']
    filter_merge_data = pd.DataFrame(sum_test_results(sys.argv[1]), columns=columns)
    df_html = filter_merge_data.to_html(escape=False)
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>
                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                    width: 50%;
                }
                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }
                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }
                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }
                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }
                body {
                    font-family: 宋体;
                }
                h1 {
                    color: #5db446
                }
                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }
                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }
                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }
                h4 {
                    color: #5db446;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }
                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }
            </STYLE>
        </head>
    """
    body = \
        """
        <body>
        <div align="center" class="header">
            <!--标题部分的信息-->
            <h4 align="center">表格中的数据为{day}自动化测试执行后的汇总信息,详细信息请查看附件!</h4>
        </div>
        <hr>
        <div class="content">
            <!--正文内容-->
            <h2> </h2>
            <div>
                {df_html}
            </div>
            <hr>
            <p style="text-align: center">
            </p>
        </div>
        </body>
        """.format(day=datetime.now().strftime("%Y-%m-%d-%H"), df_html=df_html)

    html_msg = "<html>" + head + body + "</html>"
    html_msg = Godsaycolor(filter_merge_data, html_msg, 3)
    html_msg = html_msg.replace('\n', '').encode('utf-8')
    return html_msg


if __name__ == '__main__':
    print(send_mail_excel_result())