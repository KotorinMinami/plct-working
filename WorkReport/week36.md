# 7.10~7.16 工作报告
- 同步之前提交到mugen-riscv中的自开发脚本更新，[commit](https://github.com/KotorinMinami/mugen-riscv/commit/a40c576deb1d7d6cf345fb0246695c826c606add)
- 对mugen x86 fail的一些样例进行分析，结果如下：
## fail原因一致
- os-basic
- - oe_test_auditctl：qemu镜像中均未预装audit软件，安装后测试可通过
- - oe_test_whereis：mugen脚本问题，两者whereis --help的结果一致，但与其grep结果不一致
- - oe_test_system_log_recorded：mugen脚本没有考虑/run/log/journal/中无文件夹以及不止一个文件夹的情况
- - oe_test_sos：环境语言问题影响，expect无法做出相应行为
- - oe_test_server_squid_blacklist：两者均存在黑名单添加失败的情况
- - oe_test_server_openssh_verifykey：setsebool命令未安装
## 两者在正常情况下失败原因一致，但riscv下也仍有缺陷
- os-basic
- - oe_test_dmraid：默认情况下qemu环境中/dev/mapper中无对应的设备块文件可供测试，riscv下出现dmraid -h时出现core dump的情况
- - oe_test_catman：x86下catman 1无其grep的输出，riscv下初始情况下/var/cache/man文件夹下无文件，重装man-db后软件行为正常，但同样无其所grep的输出
## 在riscv下重测通过
- os-basic
- - oe_test_power_powertop_powerup
- - oe_test_power_powertop2tuned_optimize
## fail原因不一致
- os-basic
- - oe_test_uname
- - - riscv：mugen脚本没有riscv架构的适配;
- - - x86：hostname软件未安装