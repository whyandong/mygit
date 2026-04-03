Kylin
1. 修改工具执行权限:    chmod 777 *
2. 获得管理员权限:    sudo su
3. 获得执行应用的权限:   setstatus softmode
4. 进入 ec_ram_v1.2修改makefile里的KDIR :=后面的内核版本号（例如：4.19.0），进入/usr/src路径下查看内核版本号
5.make
6. 加载ecram驱动:insmod ec_ram_dev.ko
7.cd s3s4test_v2.0
8./s3s4_test s3 [total count] (delay time) 

UOS:
1. 修改工具执行权限:    chmod 777 *
2. 获得管理员权限:    sudo su
3. 获得执行应用的权限:   set status softmode
4.进入rc_ram_v1.2 编辑makefile文件，修改KDIR :=后面的内核版本号（例如：4.19.0），使用uname -a查询内核版本号
5.make
6. 加载ecram驱动:insmod ec_ram_dev.ko
7.cd s3s4test_v2.0
8./s3s4_test s3 [total count] (delay time) 