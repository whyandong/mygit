```
#######################################################
# 框架版本：python3.7.3 + allure2.13.5
# 说明：更新平台自动化测试
#######################################################

更新平台操作系统运行指南:
    1.执行框架脚本web_updateplatform/resource/tools/auto_envion_deploy/auto_envion_deploy.sh
    2.执行框架脚本resource/rsa_crt/crt_deploy.sh
    3.重启
    4.重启后执行: python3 pytest_runner.py (不要用sudo权限执行)

运行配置基本信息:
    1.在execute.txt 配置需要运行的用例
    
      python3 pytest_runner.py
      
    2.运行脚本后生成测试报告
    
      allure open allure-report


工程架构图:
web_updateplatform
├── allure-report # allure测试报告
├── data   # 接口测试数据
├── configs 
│   └── data_config.xml  # 存放配置⽂件
├── frame
│   ├── allure_report.py  # 处理history文件，allure生成趋势报告
│   ├── connect_mysql.py  # 封装链接数据库
│   ├── constant.py  # 接口测试数据路径
│   ├── get_apt_token.py  # 封装生成token值
│   ├── get_case.py  # 获取用例路径
│   ├── get_config.py  # 获取/configs/data_config.xml配置信息
│   ├── get_login.py  # 封装登录更新平台接口
│   └── read_json.py  # 读取测试测试数据
│   └── get_redis:链接redis
    └── sha256.py:封装加密算法

├── log  # 存放打印日志的目录
├── resource
│   ├── tools
│   │   ├── auto_envion_deploy  # 测试环境搭建数据
│   ├── UnionTest框架说明文档.pdf
│   └── UnionTest V3_1_1 变更说明.docx
├── script  # 自动化测试用例case
├── execute.txt  # 执行用例路径保存位置
├── skip_list.txt  # 跳过例路径保存位置
├── pytest.ini  # 日志格式
├── pytest_runner.py # 运行文件
├── conftest.py  # 插件，重写pytest_runtest_makereport，实现了测试结果实时获取功能
├── README.md

```
