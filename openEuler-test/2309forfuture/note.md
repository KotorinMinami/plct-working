# Mugen 测试例可用性评估

## yasm

### oe_test_yasm_01

- 23.09失败原因：未安装ld指令,安装ld指令后执行失败

- 原因分析：测试例中使用yasm编译一个x86的asm文件，并执行已检验yasm的正确性，但在riscv架构中，本测试例在ld阶段就会报错，并且之后的运行也是不合理的，故此样例暂时不适合在riscv下运行

- 后续处理：可提交issue新增支持riscv架构的yasm汇编文件

## libtommatch

### oe_test_service_libtommath

- 23.09失败原因：未安装gcc,安装gcc后可通过测试

## transfig

### oe_test_transfig

- 23.09失败原因：软件更新导致输出信息与mugen预期结果不一致

- 后续：提交issue修改测试例进行兼容

## intel-cmt-cat

### oe_test_intel_cmt_cat

- 源内无此软件包

## mkfs

### oe_test_mkfs_001

- 23.09失败原因：mkfs.xfs需要至少300MB的磁盘空间，但测试例中只创建了200MB的磁盘空间

- 后续：提交issue修改测试例

## k3s

### oe_test_k3s_deployment_guide

- 23.09失败原因：与x86相同，chcon -u system_u -r object_r -t container_runtime_exec_t ${BIN_DIR}/k3s时提示chcon: can't apply partial context to unlabeled file '/usr/local/bin/k3s'怀疑为上游打包时权限问题

## procps-ng-pwdx

### oe_test_procps-ng-pwdx

- 23.09失败原因：未安装gcc指令。

## stalld

### oe_test_service_stalld

- 23.09失败原因：源中无此软件包可供安装

## aosp

### oe_test_service_aops-ceres

- 23.09失败原因，软件未预装

## struts

### oe_test_struts_001

- 23.09失败原因：与riscv相同，执行后确实对应log,需要进一步分析可用性

## smoke-OVS

### oe_test_OVS

- 23.09失败原因：openvswitch的spec存在问题，不构建dpdk子包时，安装列表中缺少ovs-vswitchd文件，导致服务启动失败

- 后续：应为缺陷，需提交issue请求修复该bug

## python-rsa*

### oe_test_python3-rsa_*

- 23.09失败原因：安装python-rsa后，对应测试的可执行文件为pyrsa-*，而脚本中执行的是pyrsa-*-3,不匹配，怀疑为版本更新导致

## procps-ng-pwdx

### oe_test_procps-ng-pwdx

- 23.09失败原因：未安装gcc指令,安装后运行超时，发现脚本编写具有缺陷，没有使用nohup指令使程序在后台运行，导致脚本一直阻塞直至超时

- 后续：提交issue修改测试例

## pwgen

### oe_test_pwgen_01

- 23.09失败原因：源中无此软件包可供安装

## mpg123

### oe_test_mpg123

- 23.09失败原因：默认自动脚本中无声卡配置项，需手动配置测试

## libx11

### oe_test_libx11

- 23.09失败原因：gcc未安装，安装后测试通过


## libpng12

### oe_test_libpng12

- 23.09失败原因：源中无此软件包可供安装(包含x86)

## libcroco

### oe_test_libcroco

- 23.09失败原因：源中无此软件包可供安装(包含x86)

## firebird

### oe_test_service_firebird-superserver

- 23.09失败原因： 安装后对应的systemd模块与mugen脚本指定的不一致，x86上也是，可能为mugen脚本抑或软件更新原因
 