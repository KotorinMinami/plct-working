# 6.19~7.25 工作报告
## mugen测试错误分析
### 缺陷
#### smoke-basic-os
- oe_test_rpm_suffix_name
- - dnf list 获取的oetestsuite 软件仓中软件包版本号不带有oe2303的规范
#### podman
- oe_test_podman_25
- - 运行docker相关指令时 fatal error: lfstack.push
- oe_test_podman_28
- - 同上
- oe_test_podman_DK_25
- - 同上
- oe_test_podman_DK_28
- - 同上
### mugen测试例问题
#### os-storage
- oe_test_storage_ext3_mount_write
- - 在分盘后使用相应盘块的变量名引用错误
- oe_test_storage_ext4_mount
- - 同上
- oe_test_storage_fileCMD_mkfs
- - 同上
### 软件包没有预装
#### spawm-fcgi
- oe_test_service_spawn-fcgi
- - 未安装initscripts
### 软件包不在源中
#### storm
- 测试需要apache-zookeeper软件包，但其并不在源中

## mugen测试
- 对应[仓库](https://github.com/KotorinMinami/res_list/blob/master/NeedTest/rest3)中测试例，并上传至res_list，[commit](https://github.com/KotorinMinami/res_list/commit/08a2e42303a151e309bbc86659138267eedad3f8)
