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

## aops

### oe_test_service_aops-ceres

- 23.09失败原因，软件未预装

## struts

### oe_test_struts_001

- 23.09失败原因：与x86相同，执行后对应相同log,需要进一步分析可用性

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

## cowsay

### oe_test_cowsay

- 23.09失败原因：源中无此软件包可供安装

## etmemd

### oe_test_etmem_001

- 23.09失败原因：x86上报错一致，暂认为测试套件存在问题

## hyperscan

### oe_test_hyperscan_simplegrep

- 23.09失败原因：源中无此软件包可供安装

## dim

### oe_test_dim_measure_001

- 23.09失败原因:缺失内核模块kvdo

### oe_test_dim_measure_002

- 23.09失败原因:gcc未安装

## cri-o

### oe_test_service_crio

- 23.09失败原因：源中无此软件包可供安装

## python-wheel

### oe_test_python-wheel_python2-wheel_command

- 23.09失败原因：源中无此软件包可供安装

## rootsh

重测通过

## nodejs-clean-css

### oe_test_cleancss_01

- 23.09失败原因：yum whatprovides显示nodejs-clean-css提供了cleancss,但实际安装后cleancss命令未在PATH中，x86亦然

### oe_test_cleancss_02

- 23.09失败原因：yum whatprovides显示nodejs-clean-css提供了cleancss,但实际安装后cleancss命令未在PATH中，x86亦然

## assimp

### oe_test_assimp_01

- 23.09失败原因：yum whatprovides显示assimp提供了assimp,但实际安装后assimp命令未在PATH中，x86亦然

### oe_test_assimp_02

- 23.09失败原因：yum whatprovides显示assimp提供了assimp,但实际安装后assimp命令未在PATH中，x86亦然

## novnc

### oe_test_novnc

- 23.09失败原因：脚本中expect语句影响，vncserver启动失败，导致后续测试失败，功能正常

- 后续：需提交issue讨论如何修改

## keepalived_cli

### oe_test_keepalived_cli

- 23.09失败原因：脚本中suite2cases配置文档中无多机器信息，鉴定为此测试例无法正常使用

## httplib2

### oe_test_httplib2

- 23.09失败原因：源中无软件包python2-httplib2

## docker-engine

### oe_test_service_docker

- 23.09失败原因：脚本问题，没有处理输出的双引号

## derby

### oe_test_service_derby

- 23.09失败原因：systemctl stop derby时停止apache derby network service超时导致报错信息

## conntrack-tools

### oe_test_service_conntrackd

- 23.09失败原因：默认配置文件无法满足启动条件，同x86

## Keras

### oe_test_Keras

- 23.09失败原因：未安装numpy,pip install tensorflow失败,提供的链接中并无riscv可用的tensorflow包或者pip存在问题，无法从对应镜像站中下载到对应的tensorflow包

## boom-boot

### oe_test_boom_boot_01

- 23.09失败原因：脚本问题，脚本指令参数次序无法被23.09的boom解析，怀疑为软件更新导致，而且新版本可能不允许配置文件无对应文件，x86同

### oe_test_boom_boot_02

- 23.09失败原因：脚本问题，脚本指令参数次序无法被23.09的boom解析，怀疑为软件更新导致，而且新版本可能不允许配置文件无对应文件，x86同

### oe_test_boom_boot_03

- 23.09失败原因：脚本问题，脚本指令参数次序无法被23.09的boom解析，怀疑为软件更新导致，而且新版本可能不允许配置文件无对应文件，x86同

## StratoVirt_user_guide

### oe_test_manage_stratovirt_vm

- 23.09失败原因：架构相关，目前无riscv64可用的vmlinux.bin，以及无软件包stratovirt

### oe_test_manage_stratovirt_vm_resources

- 23.09失败原因：架构相关，目前无riscv64可用的vmlinux.bin，以及无软件包stratovirt

### oe_test_ready_environment

- 23.09失败原因：架构相关，目前无riscv64可用的vmlinux.bin，以及无软件包stratovirt

## mailman

### oe_test_service_mailman

- 23.09失败原因：同x86,怀疑软件更新或对应链接未建立，在安装mailman后无mailman.service文件但存在mailman3.service文件

## pcs

### oe_test_service_pcs_snmp_agent

- 日志显示成功，为mugen运行是对结果统计错误

- 结论：样例可用

## whois

### oe_test_whois_03

- 23.09失败原因：脚本问题，grep字段为‘A short decription related to the object’ 实际上 description 拼写错误

- 结论：需要提交issue

## sassc

### oe_test_sassc_01

- 23.09失败原因：同x86，sassc -m 参数解析需要为 ‘-minline’ 脚本中为 ‘-m inline’ 此时sassc 会将inline解析为路径

- 结论：需要提交issue讨论具体情况

## openmpi

### oe_test_openmpi_single_01

- 23.09失败原因：x86中无法找到ompi-dvm软件包导致失败，使用dnf provides也无法找到，怀疑已被移除，riscv存在mpiexec无法正确执行mpicc编译出来的软件的情况，报错为mca_base_component_repository_open: unable to open mca_pmix_ext3x: /usr/lib64/openmpi/lib/openmpi/mca_pmix_ext3x.so: undefined symbol: pmix_value_load (ignored)

- 结论：需要提交issue

### oe_test_openmpi_single_02

- 23.09失败原因：同x86,openmpi中包含软件包与之前有所不同，导致对应测试失败

### oe_test_openmpi_cluster

- 23.09失败原因：同x86,openmpi中包含软件包与之前有所不同，导致对应测试失败

## nbdkit

### oe_test_nbdkit_02

- 23.09失败原因：同x86，nbdkit --selinux-label system_u:object_r:svirt_t:s0 example1 报错 selinux-label: setsockcreatecon_raw: Invalid argument

## itstool_2.0.4

### oe_test_itstool_2.0.4

- 23.09失败原因：同x86报错

## jython

### oe_test_jython_03

- 手动未复现，复测也通过，测试例可用




