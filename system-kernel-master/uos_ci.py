# coding:utf-8
import os
import sys
import csv
import json
import time
import argparse
import subprocess
from copy import deepcopy
from collections import namedtuple
# ut002037新增
from frame.constant import execute_file

ser_ip = ""
ser_port = ""
line = "stable"
app = "system"
ser_url = "https://ci.uniontech.com/monitor"
all_case = []
response_file = "ci-health.json"
run_file = execute_file
result_file = "ci_result.json"
case_csv = "case_list.csv"

# ut002037 新增
json_template = {
    "appName": "project_name",
    "source": "CRPCI",
    "arch": "",
    "buildLocaltion": "wuhan",
    "checkName": "ATtest",
    "checkResult": "0,0,0%",
    "checkStatus": "success",
    "buildURL": "jenkins构建地址",
    "startTime": 1111111,
    "endTime": 1111111,
    "version": 1050
}

project_array = ["system", "cve", "linglong", "secirity"]


def set_env():
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = "unix:path=/run/user/1000/bus"
    os.environ['XDG_RUNTIME_DIR'] = "/run/user/1000"
    os.environ['DISPLAY'] = ":0"
    os.environ['USER'] = ":uos"
    os.environ['QT_LINUX_ACCESSIBILITY_ALWAYS_ON'] = "1"
    os.environ['QT_ACCESSIBILITY'] = "1"
    os.system(
        "gsettings set org.gnome.desktop.interface toolkit-accessibility true")


def execute_dbus_job():
    # 指定从UnionTestConfig.json获取运行执行文件ci-health-run.txt
    command = "python3 pytest_runner.py -md ci-case-health"
    print(f"command: {command}")
    exec_code = os.system(command)
    time.sleep(1)
    # os.system(f"rm {run_file}")
    time.sleep(1)
    if not exec_code == 0:
        print("运行AT工程失败")
        sys.exit(1)


def analysis_dbus_report():
    pwd = os.getcwd()
    csv_path = pwd + '/allure-report/data/suites.csv'
    print(csv_path)
    passed_command = 'grep -w passed %s | wc -l' % csv_path
    failed_command = 'grep -w failed %s | wc -l' % csv_path
    broken_command = 'grep -w broken %s | wc -l' % csv_path
    passed = subprocess.getoutput(passed_command)
    failed = subprocess.getoutput(failed_command)
    broken = subprocess.getoutput(broken_command)
    return passed, failed, broken


def analysis_report(project_name, json_template, start_time, end_time):
    dbus_passed = int(analysis_dbus_report()[0])
    dbus_failed = int(analysis_dbus_report()[1])
    dbus_broken = int(analysis_dbus_report()[2])
    dbus_total = dbus_passed + dbus_failed + dbus_broken
    report_failed_rate = str('%.1f' % (dbus_failed / dbus_total * 100)) + '%'
    data = '%s,%s,%s' % (str(dbus_failed), str(dbus_total), report_failed_rate)
    if project_name == "deepin-authentication":
        project_name = "deepin-authenticate"
    subproject_version = subprocess.getoutput(
        f"apt list {project_name}" +
        "| awk -F ' ' '{if($0~\"已安装\")print $2}'").split('\n')[-1]
    json_template["appName"] = project_name
    json_template["checkResult"] = data
    json_template["startTime"] = start_time
    json_template["endTime"] = end_time
    json_template["version"] = subproject_version
    # ut002037新增系统架构获取
    passed_command = 'dpkg - -print - architecture'
    json_template["arch"] = subprocess.getoutput(passed_command)

    json_tem = json.dumps(json_template)
    print(json_tem)
    file_name = project_name + '_at.json'
    with open(file_name, 'w') as f:
        f.write(json_tem)


def filter_case():
    if os.path.exists(response_file):
        os.remove(response_file)

    csv_header = []
    # 读取首行
    with open("case_list.csv", "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            csv_header = row
            break

    # 读取case_list数据到列表t_list
    t_list = []
    with open("case_list.csv", "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        # 根据表头生成结构体,并根据传入模块名称获取所需测试用例
        Row = namedtuple('Row', next(f_csv))
        for each_row in f_csv:
            row_info = Row(*each_row)
            all_case.append(row_info.用例ID)
            if row_info.用例模块 == app:
                t_list.append(each_row)

    # 提交待运行测试case表单到服务器
    case_csv = f"{int(time.time())}_{app}.csv"
    with open(case_csv, "w", encoding="utf-8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(csv_header)
        f_csv.writerows(t_list)
    # 提交要运行的case到服务器
    command = f'''curl -X POST {ser_url}/v1/upload/csv/case -F "file=@./{case_csv}" \
    -H "Content-Type: multipart/form-data" -F 'app={app}' -F 'line={line}' > ci-health.json'''
    print(f"command: {command}")

    exec_code = os.system(command)
    time.sleep(1)
    if not exec_code == 0:
        print("命令执行失败")
        sys.exit(1)

    if not os.path.exists(response_file):
        print(f"{response_file}未生成")
        sys.exit(1)

    else:
        try:
            with open(response_file, "r", encoding="utf-8") as f:
                response_data = json.load(f)
        except Exception:
            print(f"{response_file}解析失败")
            command = f"cat {response_file}"
            print(f"command: {command}")
            print("=" * 20)
            os.system(command)
            time.sleep(1)
            print()
            print("=" * 20)
            sys.exit(1)

    if not response_data['code'] == 200:
        print("response_data: ", response_data)
        print("服务器出错")
        sys.exit(1)

    run_case = response_data['data']
    if not run_case:  # 无可运行case
        print("response_data: ", response_data)
        print("无待执行case")
        sys.exit(1)

    # 将待跑case写入配置的执行文件
    with open(run_file, "w", encoding="utf-8") as f:
        f.writelines(os.linesep.join(run_case))
    os.system(f"rm {response_file}")


def run():
    command = f"python3 runner.py -f {run_file}"
    print(f"command: {command}")
    exec_code = os.system(command)
    time.sleep(1)
    os.system(f"rm {run_file}")
    time.sleep(1)
    if not exec_code == 0:
        print("运行AT工程失败")
        sys.exit(1)


def send_result():
    template = {
        "steps": {
            "setup": {
                "result": "None",
                "longrepr": "None"
            },
            "call": {
                "result": "None",
                "longrepr": "None"
            },
            "teardown": {
                "result": "None",
                "longrepr": "None"
            }
        },
        "result": "pass",
        "longrepr": "None"
    }

    print("上传结果")
    if not os.path.exists(result_file):
        print(f"{result_file}未生成")
        sys.exit(1)

    total_result_dict = {}

    with open(result_file, "r", encoding='utf-8') as j:
        gs_result = json.load(j)
        for k in gs_result:
            t = deepcopy(template)
            t["result"] = gs_result[k]["result"]
            t["longrepr"] = gs_result[k]["longrepr"]
            if k in all_case:
                total_result_dict[k] = t

            if f"/{k}" in all_case:
                total_result_dict[f"/{k}"] = t
            elif k in all_case:
                total_result_dict[k] = t

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(total_result_dict, f)

    command = f'''curl -X POST {ser_url}/v1/upload/json/result -F 'file=@"{result_file}"' \
        -H "Content-Type: multipart/form-data" -F 'app={app}' -F 'line={line}' > {response_file}'''
    print(f"command: {command}")

    exec_code = os.system(command)
    time.sleep(1)
    if not exec_code == 0:
        print("命令执行失败")
        # 此处不退出
    command = f"cat {response_file}"
    print(f"command: {command}")
    print("=" * 20)
    os.system(command)
    time.sleep(1)
    print()
    print("=" * 20)
    os.system(f"rm {response_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='execute testcases')
    parser.add_argument('--app', dest='app', default='', help='app name')
    parser.add_argument('--line', dest='line', default='', help='仓库标签')
    parser.add_argument('--ip', dest='ser_ip', default='', help='服务ip')
    parser.add_argument('--port',
                        dest='ser_port',
                        default='10086',
                        help='服务端口')
    parser.add_argument('--url', dest='ser_url', default='', help='域名')
    parser.add_argument('--clevel', dest='clevel', default='', help='用例级别')
    args = parser.parse_args()

    if args.ser_url:
        ser_url = args.ser_url
    else:
        if args.ser_ip == "":
            print("参数不足")
            print("app:  ", "必填         ", args.app)
            print("line: ", "必填         ", args.line)
            print("ip:   ", "url和ip选其一 ", args.ser_ip)
            print("port: ", "默认10086    ", args.ser_port)
            print("url:  ", "url和ip选其一 ", args.ser_url)
            print("clevel  ", "目前暂不处理 ", args.clevel)
            sys.exit(1)
        else:
            ser_url = f"http://{args.ser_ip}:{args.ser_port}"

    if args.app == "" or args.line == "":
        print("参数不足")
        print("app:  ", "必填         ", args.app)
        print("line: ", "必填         ", args.line)
        print("ip:   ", "url和ip选其一 ", args.ser_ip)
        print("port: ", "默认10086    ", args.ser_port)
        print("url:  ", "url和ip选其一 ", args.ser_url)
        sys.exit(1)
    else:
        app = args.app
        line = args.line

    if app not in project_array:
        print("please enter correct project name")
        sys.exit(1)

    set_env()
    start_time = int(time.time())
    filter_case()
    execute_dbus_job()
    send_result()
    end_time = int(time.time())
    analysis_report(app, json_template, start_time, end_time)
