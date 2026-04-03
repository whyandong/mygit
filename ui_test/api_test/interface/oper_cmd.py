# -*- coding: utf-8 -*-

import os
import yaml
import time

class SystemOper:
    #获取命令行信息
    def command_return_info(self, cmd):
        if len(os.popen(cmd).readlines()) == 1:
            tmp = str(os.popen(cmd).readline()).strip()
        else:
            tmp = str(os.popen(cmd).read().strip())
        return tmp

    #获取打印机驱动默认集成清单结果
    def check_printer_driver(self, file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['printer_driver_list']:
            line = line.strip()
            packagename = line.split('_')[0]
            cmd = "dpkg -l %s |grep ii" % packagename
            tmp = self.command_return_info(cmd)
            if tmp != '':
                cmd = "dpkg -l %s |grep ii|awk  '{print $3\"_\"$4}'" % packagename
                version_info = self.command_return_info(cmd)
                packageinfo = packagename + '_' + version_info + '.deb'
                if line == packageinfo:
                    result_list.append('passed')
                else:
                    result_list.append(packageinfo)
            else:
                result_list.append()
        deb_file.close()
        return result_list

    #系统软件包状态检查
    def check_package(self):
        result_list = []
        cmd = 'dpkg -l | grep -v "^ii" | wc -l'
        tmp = self.command_return_info(cmd)
        if tmp != '' and tmp == '5':
            result_list.append('passed')
        else:
            cmd = 'dpkg -l | grep -v "^ii"'
            result_list.append(self.command_return_info(cmd))
        return result_list

    #系统默认启动服务检查
    def check_system_service(self,file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['system_services']:
            line = line.strip()
            cmd = "systemctl is-active %s" % line
            tmp = self.command_return_info(cmd)
            if tmp != '':
                if tmp == 'active':
                    result_list.append('passed')
                else:
                    result_list.append(line + ' ' +  tmp)
            else:
                result_list.append(line + 'not install')
        deb_file.close()
        return result_list
    
    #系统默认使用端口检查
    def check_system_default_port(self,file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['system_default_port']:
            line = str(line).strip()
            cmd = 'lsof -i:%s | grep "(LISTEN)" | awk \'{print $1}\' | sort -n | uniq ' % line
            tmp = self.command_return_info(cmd)
            if tmp != '':
                result_list.append('passed')
            else:
                result_list.append(line + 'not use')

        deb_file.close()
        return result_list
    
    #系统常用命令检查
    def check_system_cmd(self,file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['system_cmd_list']:
            line = line.strip()
            cmd = '%s --help  2>&1' % line
            tmp = self.command_return_info(cmd)
            if tmp != '':
                if 'not found' in tmp:
                    result_list.append(line + ' 命令未集成')
                else:
                    result_list.append('passed')
        deb_file.close()
        return result_list

    #系统源文件非空检查
    def check_system_sources(self):
        result_list = []
        cmd = 'grep -c ^deb /etc/apt/sources.list'
        tmp = self.command_return_info(cmd)
        if tmp != '':
            try:
                if int(tmp) > 0:
                    result_list.append('passed')
                elif int(tmp) == 0:
                    result_list.append('系统源文件/etc/apt/sources.list为空')
            except:
                result_list.append(tmp)
        return result_list
    
    #系统信息-os-release文件
    def check_system_os_release(self, expect):
        result_list = []
        cmd = 'cat /etc/os-release |grep PRETTY_NAME'
        tmp = self.command_return_info(cmd)
        if tmp != '':
            try:
                os_release = tmp.replace('"','').split(' ')[-1]
                if os_release == expect:
                    result_list.append('passed')
                else:
                    result_list.append(os_release)
            except:
                result_list.append(tmp)
        return result_list
    
    #公网源优先级配置检查
    def check_system_sources_priority(self, expect):
        result_list = []
        cmd = 'cat /etc/apt/preferences.d/99priority'
        tmp = self.command_return_info(cmd)
        if tmp != '':
            try:
                if tmp == expect.strip():
                    result_list.append('passed')
                else:
                    result_list.append(tmp)
            except:
                result_list.append(tmp)
        return result_list

    
    #终端指令-进程、监控相关
    def check_system_cmd_monitor(self, file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['system_cmd_monitor']:
            line = line.strip()
            cmd = '%s --help  2>&1' % line
            tmp = self.command_return_info(cmd)
            if tmp != '':
                if 'not found' in tmp:
                    result_list.append(line + ' 命令未集成')
                else:
                    result_list.append('passed')
        deb_file.close()
        return result_list
    
    #终端指令-系统管理相关
    def check_system_cmd_systemctl(self, file_name):
        result_list = []
        file_name_path = os.path.join(os.getcwd(), 'testdata', file_name)
        deb_file = open(file_name_path, "r", encoding='utf-8')
        debs = yaml.load(deb_file, Loader=yaml.FullLoader)
        for line in debs['system_cmd_systemctl']:
            line = line.strip()
            cmd = '%s --help  2>&1' % line
            tmp = self.command_return_info(cmd)
            if tmp != '':
                if 'not found' in tmp:
                    result_list.append(line + ' 命令未集成')
                else:
                    result_list.append('passed')
        deb_file.close()
        return result_list

    #系统内核版本
    def check_kernel_version(self, expect):
        result_list = []
        cmd = 'uname -r | cut -d- -f1'
        tmp = self.command_return_info(cmd)
        if tmp != '':
            try:
                if tmp == expect:
                    result_list.append('passed')
                else:
                    result_list.append(tmp)
            except:
                result_list.append(tmp)
        return result_list

    #有线网络-打开关闭网络
    def control_network(self):
        result_list = []
        cmd = 'nmcli networking off'
        self.command_return_info(cmd)
        cmd = 'ping www.baidu.com -c 2 | grep received | awk -F \'[ ,]\' \'{print $5}\' 2>&1'
        tmp = self.command_return_info(cmd)
        if tmp != '':
           result_list.append(tmp)
        else:
            result_list.append('passed')
        cmd = 'nmcli networking on'
        self.command_return_info(cmd)
        time.sleep(5)
        cmd = 'ping www.baidu.com -c 2 | grep received | awk -F \'[ ,]\' \'{print $5}\' 2>&1'
        tmp = self.command_return_info(cmd)
        if tmp != '':
            try:
                if tmp == '2':
                    result_list.append('passed')
                else:
                    result_list.append(tmp)
            except:
                result_list.append(tmp)
        return result_list

#通过用例方法名获取对应的方法
def select_file(function_name, file_name='',expect=''):
    systemoper = SystemOper()
    if function_name == 'test_printer_driver' and file_name == 'printer_driver_list.yaml':
        return systemoper.check_printer_driver(file_name)
    if function_name == 'test_check_package':
        return systemoper.check_package()
    if function_name == 'test_check_system_service' and file_name == 'system_services.yaml':
        return systemoper.check_system_service(file_name)
    if function_name == 'test_check_system_default_port' and file_name == 'system_default_port.yaml':
        return systemoper.check_system_default_port(file_name)
    if function_name == 'test_check_system_cmd' and file_name == 'system_cmd_list.yaml':
        return systemoper.check_system_cmd(file_name)
    if function_name == 'test_check_system_sources':
        return systemoper.check_system_sources()
    if function_name == 'test_check_system_os_release':
        return systemoper.check_system_os_release(expect)
    if function_name == 'test_check_system_sources_priority':
        return systemoper.check_system_sources_priority(expect)
    if function_name == 'test_check_system_cmd_monitor' and file_name == 'system_cmd_monitor.yaml':
        return systemoper.check_system_cmd_monitor(file_name)
    if function_name == 'test_check_system_cmd_systemctl' and file_name == 'system_cmd_systemctl.yaml':
        return systemoper.check_system_cmd_systemctl(file_name)
    if function_name == 'test_check_kernel_version':
        return systemoper.check_kernel_version(expect)
    if function_name == 'test_control_network':
        return systemoper.control_network()