#### 接口测试框架（基于json格式、http/https请求,python3）

##### 注：现在基于Excel文件管理测试用例基本实现

###### 1.casefile文件夹存放试用例相关的

###### 2.testdata测试的驱动数据

###### 3.interface对测试接口相关的封装，包括requests库，从Excel取测试数据的封装，json断言的封装，命令执行的封装

###### 4.public 打印日志的封装，发送邮件的封装，登录获取token的接口，发送钉钉的封装

###### 5.report 存放测试报告

###### 6.pytest.ini 用例注册、管理用例标记的文件

###### 7.run_main_testcases.py  主运行文件。运行后可以生成相应的测试报告和回写测试结果到xls用例文件

###### 8.install.sh  linux 下运行接口自动化的安装脚本，需要使用sudo执行

### 自动化报告界面

![Image text](https://gitee.com/Reboencheng/api_test/raw/master/img/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A.png)

### 自动化报告邮件界面

![Image text](https://gitee.com/Reboencheng/api_test/raw/master/img/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A%E9%82%AE%E4%BB%B6.png)