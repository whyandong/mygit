# -*- coding: utf-8 -*-
import os
import subprocess
import json

import pexpect
import openpyxl

# from frame.uparser import ulog
from frame.constant import resource_root_path
from frame.constant import allure_results_path


# ****************************************************
# @Interface Description: 从shell执行cmd命令，无论命令执行成功或失败，都将获取命令返回结果
# @In: command
# @Out:  None
# @Return: 接口返回命令后的结果或者错误信息
# @Test Remark:
# @Author: ut002037
# @Date: 2021.11.29
# *****************************************************
def execute_command(command):
    """
    执行终端命令,输出内容
    :param command:输入的命令
    :return:命令执行内容输出
    """
    # cmd="echo 1 |"+"sudo -S "+command
    # print(command)
    p = subprocess.Popen(command,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8')
    out_msg = p.stdout.read()
    err_msg = p.stderr.read()

    if err_msg:
        return err_msg
    else:
        return out_msg


# ****************************************************
# @Interface Description: 权限位解析
# @In: 权限位
# @Return: 权限值
# @Test Remark:
# @Author: ut002037
# @Date: 2022.05.24
# *****************************************************
def parse_file_perssion(perm):
    tmp = perm[1:].replace("r", "4").replace("-", "0").replace(
        "w", "2").replace("x", "1").replace("s",
                                            "1").replace("S", "0").replace(
                                                "t", "1").replace("T", "0")
    if "s" in perm[1:4] or "S" in perm[1:4]:
        suid = "4"
    else:
        suid = "0"
    if "s" in perm[4:7] or "S" in perm[4:7]:
        guid = "2"
    else:
        guid = "0"
    if "t" in perm[7:10] or "T" in perm[7:10]:
        tuid = "1"
    else:
        tuid = "0"
    first = str(int(suid) + int(guid) + int(tuid))
    second = str(int(tmp[0]) + int(tmp[1]) + int(tmp[2]))
    third = str(int(tmp[3]) + int(tmp[4]) + int(tmp[5]))
    fourth = str(int(tmp[6]) + int(tmp[7]) + int(tmp[8]))
    if first == "0":
        return second + third + fourth
    else:
        return first + second + third + fourth


# ****************************************************
# @Interface Description: 打开一个excel文件，根据sheet名返回sheet对象用于操作该sheet页
# @In: excel文件路径
# @In: sheet页名称
# @Out: return 输入sheet页的操作符
# @Return: 接口
# @Test Remark:
# @Author: ut002037
# @Date: 2022.04.21
# *****************************************************


def open_excel_file(file_path, sheet_name):
    """
    打开一个excel文件,根据传入的sheet名称进行sheet操作
    :In: excel路径
    :in: 待操作的sheet页名称sheet_name
    :Out: 系统架构
    """
    fp = openpyxl.load_workbook(file_path)
    sheet_op = fp[sheet_name]
    return sheet_op


# ****************************************************
# @Interface Description:根据文件获取所属包
# @In:  文件路径名称
# @Out: None
# @Return: 包名
# @Test Remark:
# @Author:  ut002037
# *****************************************************
def get_packet_name_from_path(path):
    cmd = "dpkg --search " + path
    packet_name = execute_command(cmd).split(":")[0]
    return packet_name


# ***********************************
# @Interface Description:根据包名获取包的版本信息
# @In:  packet_name 包名
# @Out: None
# @Return: 包的版本信息
# @Test Remark:
# @Author:  ut002037
# ***********************************
def get_packet_version(packet_name):
    cmd = "apt policy " + packet_name + " 2>/dev/null"
    version = execute_command(cmd)
    return version


# ****************************************************
# @Interface Description:修改pms_job.json的baseurl地址为本地ip,并启动该服务
# @In: None
# @Out:  None
# @Return: None
# @Test Remark:
# @Author: ut002037
# @Date: 2021.11.29
# *****************************************************
def start_pms_server():
    ip_addr_lst = execute_command("hostname -I").split(" ")
    for i in ip_addr_lst:
        if "10.20." in i:
            ip_addr = i
    service_url = f"http://{ip_addr}:3000/api/v1/zbox/result"
    with open(os.path.join(resource_root_path, 'pms', 'pms_job.json'),
              'r',
              encoding='utf-8') as f:
        base_info = json.load(f)
        base_info['baseurl'] = service_url
    with open(os.path.join(resource_root_path, 'pms', 'pms_job.json'),
              'w',
              encoding='utf-8') as f:
        json.dump(base_info, f)
    pms_service_path = os.path.join(resource_root_path, 'pms',
                                    'pms_post_server')
    os.system(f"cd {pms_service_path};./pms_result &")


# ****************************************************
# @Interface Description:获取当前平台架构
# @In:  None
# @Out: None
# @Return: 返回平台架构
# @Test Remark:
# @Author:  ut002037
# @Date: 2021.11.29
# *****************************************************
def get_platform_arch():
    """
    执行dpkg命令,获取平台架构
    :In: None
    :Out: 系统架构
    """
    sys_arch = execute_command("dpkg --print-architecture").replace("\n", "")
    if "amd" in sys_arch:
        sys_arch = "amd"
    elif "arm" in sys_arch:
        sys_arch = "arm"
    elif "mips" in sys_arch:
        sys_arch = "mips"
    elif "loongarch" in sys_arch:
        sys_arch = "loongarch"
    return sys_arch


# ****************************************************
# @Interface Description:获取当前系统版本号
# @In:  None
# @Out: None
# @Return: 返回当前系统版本号
# @Test Remark:
# @Author:  ut002037
# @Date: 2021.11.29
# *****************************************************
def get_system_version():
    """
    执行命令cat /proc/sys/kernel/uosversion获取系统版本号
    :In: None
    :Out: None
    """
    sys_version = execute_command("cat /etc/os-version |grep 'MinorVersion' |awk -F '=' '{print$2}'").replace("\n","")
    return sys_version


def get_system_version1():
    sys_version1 = execute_command(
        "cat /etc/os-version |grep 'MinorVersion' |awk -F '=' '{print$2}'"
    ).replace("\n", "")
    # sys_version=execute_command("cat /proc/sys/kernel/uosversion").replace("\n","")
    return sys_version1


# ****************************************************
# @Interface Description:抓取系统日志和内核日志
# @In: tsc_name
# @Out:  None
# @Return: 无返回值
# @Test Remark:
# @Author:  ut002037
# @Date: 2021.11.29
# *****************************************************
def system_kernel_log_cap(tsc_name):
    """
    根据测试用例名称抓取并存储失败用例的系统与内核日志
    :In: tsc_name 测试用例名称
    :Out: None
    """
    debug = False
    if not debug:
        log_dir = allure_results_path + "/" + tsc_name
        cmd = 'mkdir -p ' + log_dir
        os.system(cmd)

        cmd1 = "echo -n 1|sudo -S cp -rf /var/log/ " + log_dir
        os.system(cmd1)

        cmd2 = "echo -n 1|sudo -S cp -rf /home/$USER/kwin.log " + log_dir
        os.system(cmd2)

        cmd3 = "echo -n 1|sudo -S cp -rf /var/lib/systemd/coredump " + log_dir
        os.system(cmd3)

        cmd4 = "uname -a >" + log_dir + "/uname.log"
        os.system(cmd4)

        cmd5 = "mount>" + log_dir + "/mount.log"
        os.system(cmd5)

        cmd6 = "lspci -nn >" + log_dir + "/lspci.log"
        os.system(cmd6)

        cmd7 = "lsusb -v >" + log_dir + "/lsusb.log"
        os.system(cmd7)

        cmd8 = "echo -n 1|sudo -S lshw >" + log_dir + "/lshw.log"
        os.system(cmd8)

        cmd9 = "echo -n 1|sudo -S dmesg >" + log_dir + "/dmesg.log"
        os.system(cmd9)

        cmd10 = "echo -n 1|sudo -S dmesg -l 3 >" + log_dir + "/dmesg_err.log"
        os.system(cmd10)

        cmd11 = "echo -n 1|sudo -S tar -zcvf " + allure_results_path + "/" + tsc_name + ".tar.gz " + log_dir
        os.system(cmd11)

        cmd12 = "echo -n 1|sudo -S rm -rf " + log_dir
        os.system(cmd12)


# ****************************************************
# @Interface Description: uos用户、root用户登陆本地shell,执行命令
# @In:   cmd, expect_res
# @Out:  None
# @Return: res, step1
# @Test Remark:
# @Author:  ut003905
# @Date: 2021.11.29
# *****************************************************
def root(tsc_name):
    """
    sudo su 切换root用户
    :param: None
    :return: child即登陆句柄
    """
    child = pexpect.spawn('sudo su', encoding='utf-8')
    f = open('log/%s' % tsc_name, 'w')
    child.logfile = f
    # child.logfile_read = sys.stdout    #需配合encoding='utf-8'
    res = child.expect(["root@uos-PC:/home/uos", "请输入密码:"], timeout=120)
    if res == 1:
        child.sendline("1")
        res = child.expect("root@uos-PC:/home/uos", timeout=120)
    if res == 0:
        print("\r\n==========root用户执行命令==========")
    return child


def uos(tsc_name):
    """
    远程调试使用
    """
    child = pexpect.spawn('ssh uos@10.20.53.55', encoding='utf-8')
    f = open('log/%s' % tsc_name, 'w')
    child.logfile = f
    # child.logfile_read = sys.stdout    #需配合encoding='utf-8'
    res = child.expect([
        "Are you sure you want to continue connecting (yes/no)?",
        "(.*?) password"
    ],
                       timeout=120)
    if res == 0:
        child.sendline("yes")
        child.expect("(.*?) password", timeout=120)
    child.sendline("1")
    child.expect("uos@uos-PC", timeout=120)
    return child


def roottest(tsc_name):
    """
    远程调试使用
    """
    child = uos(tsc_name)
    child.sendline("sudo su")
    res = child.expect(["root@uos-PC:/home/uos", "请输入密码:"], timeout=120)
    if res == 1:
        child.sendline("1")
        res = child.expect("root@uos-PC:/home/uos", timeout=120)
    if res == 0:
        print("\r\n==========root用户执行命令==========")
    return child


def uos_exec_cmd(cmd, expect_res, tsc_name):
    """
    uos用户执行命令,并返回匹配值,0 表示与命令预期结果相符,1 表示与命令预期结果不相符
    :param command: cmd:执行的命令
    :param command: expect_res:期待命令返回值,ps:不同环境返回值可能不一样,为提升兼容性,此处传入list
    :return: res: 命令执行内容输出
    :return: step1: 执行结果与预期结果
    """
    child = pexpect.spawn('whoami', encoding='utf-8')
    f = open('log/%s' % tsc_name, 'w')
    child.logfile = f
    res = child.expect(['uos', "root"], timeout=120)
    if res == 0:
        child.expect("uos@uos-PC", timeout=120)
    else:
        child.sendline('su - uos')
        child.expect("uos@uos-PC", timeout=120)
    print("\r\n==========uos用户执行命令==========")
    child.sendline(cmd)
    expect_list = [*expect_res, "uos@uos-PC"]
    res = child.expect(expect_list, timeout=120)
    step1 = "step1 exec " + cmd + " return :" + child.before + '\n' + child.after + " which expect return in:" + str(
        expect_res)
    if res < (len(expect_list) - 1):
        child.expect("uos@uos-PC", timeout=120)
        child.sendline("exit")
    else:
        child.sendline("exit")
    return res, step1


def root_exec_cmd(cmd, expect_res, tsc_name):
    """
    root用户执行命令,并返回匹配值,0 表示与命令预期结果相符,1 表示与命令预期结果不相符
    :param command: cmd:执行的命令
    :param command: expect_res:期待命令返回值,ps:不同环境返回值可能不一样,为提升兼容性,此处传入list
    :return: res: 命令执行内容输出
    :return: step1: 执行结果与预期结果
    """
    # 正常运行时使用root(tsc_name)，调试时使用roottest(tsc_name)
    child = root(tsc_name)
    child.sendline(cmd)
    expect_list = [*expect_res, "root@uos-PC:/home/uos"]
    res = child.expect(expect_list, timeout=120)
    step1 = "step1 exec " + cmd + " return :" + child.before + '\n' + child.after + " which expect return in:" + str(
        expect_res)
    if res < (len(expect_list) - 1):
        child.expect("root@uos-PC:/home/uos", timeout=120)
        child.sendline("exit")
    else:
        child.sendline("exit")
    return res, step1
