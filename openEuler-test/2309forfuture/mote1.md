# Mugen 测试例可用性评估

## podman 

### oe_test_podman_0.10.1

- 测试套脚本问题，--help时grep的USAGE与实际的Usage不符，对配置文件的修改疑似使得配置出现错误，未知是否为版本更新问题所致

### oe_test_podman_01

- 官方并未给出对应RISCV架构的docker镜像,x86 失败为脚本grep字段与实际输出不同原因

### oe_test_podman_02
- 官方并未给出对应RISCV架构的docker镜像,x86 失败为脚本问题，在两个镜像的情况下没有对对应输出进行处理，导致参数混乱

### oe_test_podman_03
- 官方并未给出对应RISCV架构的docker镜像,x86失败问题未知，文件缺失，不知为配置问题或版本更新问题

### oe_test_podman_04
- 官方并未给出对应RISCV架构的docker镜像,x86失败为脚本问题，没有映射端口导致awk对应定位失效，最后导致失败

### oe_test_podman_05
- 官方并未给出对应RISCV架构的docker镜像,x86失败为脚本问题，Error: --compress can only be set when --format is 'docker-dir'，以及podman info --debug确实不会输出debug字段，grep文本不符合

### oe_test_podman_06
- 官方并未给出对应RISCV架构的docker镜像,x86失败为时区显示问题

### oe_test_podman_07
- 官方并未给出对应RISCV架构的docker镜像,x86失败为脚本问题，疑似版本更形移除或相关命令的形式改变

### oe_test_podman_08
- 官方并未给出对应RISCV架构的docker镜像,x86失败为x86内核不支持对应配置

## cppcheck

### oe_test_cppcheck

- riscv与x86失败原因一致，因为cppcheck在23.09上无法以posix标准检查文件，同时-DA --force 参数也存在问题

## nodejs

### oe_test_nodejs_04

- riscv与x86失败原因一致，因为nodejs在23.09上使用node --v8-options是打印信息中没有grep的文本

## netcdf

### oe_test_netcdf

- riscv与x86失败原因一致，源中无netcdf

## python3-keyring_13.2.1

### oe_test_keyring-python3

- riscv与x86失败原因一致，python3-keyring提供可执行文件keyring,但脚本中执行的是keyring-python3

## easymock

### oe_test_easymock_spring

- riscv与x86失败原因一致，源中无测试需要的springframework-test软件包

## clamav

### oe_test_clamav_clamdtop

- riscv与x86失败原因一致，但无法复现，可能是脚本运行时的环境差异导致

## corosync

### oe_service_spausedd

- riscv与x86失败原因一致，无软件包spausedd可供安装

## pyyaml

### oe_test_pyyaml

- riscv与x86失败原因一致，脚本中使用的python样例出现语法错误，应为python更新后导致的语法变化

## libsdl2

### oe_test_libsdl1.2

- riscv与x86失败原因一致，未预装gcc

