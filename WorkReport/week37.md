# 7.17~7.23工作报告
- 统计mugen自4月以来更新的baseOS的测试用例，进行同步测试，分析
## 分析结果
### x86failed
#### 失败原因一致
- amanda
- - oe_test_amanda_dump:出错的指令报错一致
- kernel
- - oe_test_fnic:内核模块fnic未编译，故无法测试
- - oe_test_hifc:内核模块hifc未编译，故无法测试
- - oe_test_libfc:内核模块libfc未编译，故无法测试
- os-basic
- - oe_test_bunzip2:mugen脚本问题，脚本创建文件与使用文件路径不一致
- - oe_test_csplit:mugen脚本问题，在x86与riscv上都可确认csplit产生的文件的位置应为当前目录，而非文本目录
- - oe_test_ctags:均未预装ctags指令，安装后可通过
- - oe_test_libsecret:没有使用有gui的镜像，$DISPLAY无对应值，不支持测试
- plymouth
- - oe_test_service_plymouth-switch-root-initramfs:systemd单元启动失败，Condition check resulted in Tell Plymouth To Jump To initramfs being skipped.
- sendmail
- - oe_test_sendmail_func_001:软件lsof未安装
#### 根本失败原因一致，但存在其他因素
- libtiff
- - oe_test_libtiff:没有安装libtiff-devel软件包，tiffio.h文件缺失
- - - x86:未安装gcc
- os-basic
- - oe_test_audit_02:mugen脚本使用的比较过时的service管理体系
- - - riscv：没适配service xxx start的指令
- - - x86：报错无对应的service unit

### failed
#### 缺陷
- iSulad
- - oe_test_iSulad_resource_mapping:镜像pull失败，提示：Failed to pull image centos with error: fetch and parse manifest failed
- - oe_test_iSulad_resource_restriction_cgroup:镜像pull成功，但启动容器失败
- net-tools
- - oe_test_net-tools_iptunnel:软件运行失败，原因未知，提示ioctl: No such device
### 内核未编译
- kernel
- - oe_test_nbd:内核模块nbd未编译
- - oe_test_qla2xxx:内核模块qla2xxx未编译
### 软件未预装
- os-basic
- - oe_test_envsubst:软件gettext未安装
