# 具体发现
## os-storage
- oe_test_storage_smb_cmd_smbpasswd
- - 运行软件smbpassword时需要加载libmessages-util-samba4.so，在LD_LIBRARY_PATH环境变量相同时，x86环境下运行可自动找到对应文件，但riscv下无法找到，只有将对应lib的文件路径赋值到环境变量时才可正常运行
- oe_test_storage_smb_cmd_testparm
- - 运行软件时需要加载libserver-role-samba4.so，在LD_LIBRARY_PATH环境变量相同时，x86环境下运行可自动找到对应文件，但riscv下无法找到，只有将对应lib的文件路径赋值到环境变量时才可正常运行
- oe_test_storage_smb_cmd_smbcontrol
- - 运行软件时需要加载libmessages-util-samba4.so，在LD_LIBRARY_PATH环境变量相同时，x86环境下运行可自动找到对应文件，但riscv下无法找到，只有将对应lib的文件路径赋值到环境变量时才可正常运行
- oe_test_storage_smb_cmd_smbstatus
- - 运行软件时需要加载libmessages-util-samba4.so，在LD_LIBRARY_PATH环境变量相同时，x86环境下运行可自动找到对应文件，但riscv下无法找到，只有将对应lib的文件路径赋值到环境变量时才可正常运行
- oe_test_storage_smb_guest_share
- - 同理，不过上面两个lib文件都需加载
- oe_test_storage_fileCMD_pwd
- - 文件系统中并没有选择测试的目录，使用mkdir事先建立对应目录可过，建议加入pre_test中
## smoke-basic-os
- oe_test_user_debug_iotop_03
- - 当前环境不支持软件运行，怀疑为内核问题
    ```
    [root@openeuler-riscv64 ~]# iotop -o -b -n 1 -d 10
    Could not run iotop as some of the requirements are not met:
    - Linux >= 2.6.20 with
    - I/O accounting support (CONFIG_TASKSTATS, CONFIG_TASK_DELAY_ACCT, CONFIG_TASK_IO_ACCOUNTING)
    ```
## samba
- oe_test_service_smb
- - 同上os-storage中与samba有关样例，无法获取的lib文件为：libmessages-util-samba4.so
- oe_test_service_nmb
- - 同上os-storage中与samba有关样例，无法获取的lib文件为：libmessages-util-samba4.so
- oe_test_service_winbind   
- - 同上os-storage中与samba有关样例，无法获取的lib文件为：libflag-mapping-samba4.so


# 软件未安装
## os-storage
- dracut
## smoke-basic-os
- glibc-devel
- os-prober
- rsyslog
- lshw
- dmidecode

# 内核模块问题
## smoke-basic-os
- tcp_bbr
    ```
    [root@openeuler-riscv64 ~]# sudo modprobe tcp_bbr
    modprobe: FATAL: Module tcp_bbr not found in directory /lib/modules/6.1.19-2.oe2303.riscv64
    ```
- bonding
    ```
    + modprobe bonding
    modprobe: FATAL: Module bonding not found in directory /lib/modules/6.1.8-3.oe2303.riscv64
    ```
# 源内無对应软件
## smoke-basic-os
- oe_test_criu: criu
    ```
    [root@openeuler-riscv64 ~]# yum install criu -y
    Last metadata expiration check: 0:35:42 ago on 2023年05月25日 星期四 16时35分28秒.
    No match for argument: criu
    Error: Unable to find a match: criu
    ```