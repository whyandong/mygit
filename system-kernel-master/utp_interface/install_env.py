# coding:utf-8
import os
import stat

file_dir_path = os.path.dirname(os.path.abspath(__file__))  # 文件所在路径
root_path = os.path.dirname(file_dir_path)  # 文件所在路径

os.chdir(file_dir_path)
if not os.path.exists(os.path.join(file_dir_path, 'utp_log')):
    os.mkdir('utp_log')
    os.chmod('utp_log', stat.S_IRWXO | stat.S_IRWXU | stat.S_IRWXG)
os.chdir(root_path)

install_script = os.path.join(
    root_path, 'resource/tools/auto_envion_deploy/install_env.py')
os.system(f"python3 {install_script}")
