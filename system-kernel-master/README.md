# 一、dbus测试环境自动化部署说明
***
1. 安装pip3：sudo apt-get install python3-pip


2. 一键部署环境:cd 到工程目录resource/tools/auto_envion_deploy下执行sudo sh auto_envion_deploy.sh

# 二、dbus测试执行
***

3. 脚本执行方式一,全量执行:python3 pytest_runner.py 默认执行所有execute.txt里面所有用例

4. 脚本执行方式二,按模块执行: python3 pytest_runner.py -md _modulename_,*modulename*可选值为dde-api,dde-daemon,lastore-daemon等后端项目名称
例如执行python3 pytest_runner.py -md dde-api 运行dde-api模块用例

# 三、dbus测试调试
***
5. 调试单个或多个用例：从resource/tools/caselist 里面copy 想要执行的dbus脚本到execute.txt即可

   如：\script\dbus\systemBus\soundThemePlayer\001_enableSoundDesktopLogin.py


# 四、dbus测试日志查看
***

6. 日志查看：jenkins执行直接看allure报告。本地执行，需要将pytest_runner.py os.system(f"allure generate --clean {allure_results_path} -o {allure_report_path}")代码放开注释，cd 到allure-report目录里面，终端执行 allure open . 查看。

# 五、dbus/gsettings分支代码管理规范
***

   **1.命名规范**
***

>**dbus项目分为三个架构，分别采取dev+*版本名*+*架构名的方式***

   >例如:

   >>dev-1050 ----1050版amd64架构，不带架构名称默认为amd64位

   >>dev-1050-arm ----1050版arm64架构

   >>dev-1050-mips ----1050版mips64架构

>**gsettings项目只有一个架构，命名为dev+gsetting+*版本号***

   >>1050版本:dev-gsetting-1050

   >>1040版本:dev-gsetting-sp4

>**集中域管依赖接口分支名为dev-1050-admanager**

**2.管理规范**
***

   当DDE项目处于1050版本测试阶段时，dbus，gsettings与之匹配的自动化代码分支为带有1050字符的命名分支，当UOS 1050版本发布   后，自动化代码分支会根据新
  的版本名称来命名分支 ，例如，*dev-1060*等，跟随**UOS版本名称**取名。将原来的分支打上tag后，不再更新。

**3.维护规范**
***

   增加/删除/维护用例，函数时，commit信息必须携带具体操作描述，add/update/fix/delete/(模块名:简要描述信息)

**4.代码开发规范**
***

  参考wiki链接:*https://wikidev.uniontech.com/Dbus%E5%90%8E%E7%AB%AF%E8%87%AA%E5%8A%A8%E5%8C%96%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83*