# Mugen riscv并入上游要点
## 现状
> Todo：整理证据，报告
### 并入的重要性
### 目前相较于mugen上游的做出的成果
- 经过验证mugen的大部分脚本可以直接适用于openEuler-RISCV qemu的自动化测试:[openEuler 23.09 RISC-V 测试报告](https://gitee.com/yunxiangluo/open-euler-risc-v-23.09-test/tree/master)
- 经过开发编写以及实测验证，已经开发了针对RISCV与x86架构的qemu镜像可在PC设备上进行自动多线程测试的脚本:[介绍](https://github.com/weilinfox/PLCT-Working/blob/master/Note/mugen-tech/mugen%20%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E5%A5%97%E4%BB%B6%E2%80%94%E2%80%94%E7%BC%BA%E9%99%B7%E3%80%81%E6%94%B9%E8%BF%9B%E4%B8%8E%E5%B1%95%E6%9C%9B.pptx)
- 针对目前所有mugen的脚本，已经有针对出现兼容性问题的脚本进行分析的结果，具体修改方案待商榷
### 兼容性以及RISCV目前的问题
- mugen上游的脚本仍有一些具有兼容性问题其中包括但不限于：

- - mugen suite2case 配置中对环境要求的描述不准确：

- - - [rsyslog/oe_test_rsyslog_abnormal_template.sh](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/rsyslog/oe_test_rsyslog_abnormal_template/oe_test_rsyslog_abnormal_template.sh) 这一测试用例需要 NODE2 配置，即需要 2 个节点进行测试，但是 [rsyslog.json](https://gitee.com/openeuler/mugen/blob/master/suite2cases/rsyslog.json) 中没有 "machine num" 配置。这一问题在该测试套共影响 10 个测试用例
- - - [lvm2oe_test_lvm2_pvdisplay_001](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/lvm2/oe_test_lvm2_pvdisplay_001.sh),此样例使用check_free_disk函数检测空闲磁盘，但suite2case中没有配置add disk信息，导致此测试用例失败

- - mugen脚本对于测试环境的准备标准各有差异

- - - [mc/oe_test_mc_base_01](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/mc/oe_test_mc_base_01.sh) ``grep 'Home路径'`` 尝试 grep 中文字串，实际输出为 ``Home directory``,实为语言环境问题
- - - [kernel/oe_test_swap_compress](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/kernel/oe_test_swap_compress.sh) 测试使用的 swap 设备 ``/dev/dm-1`` 没有提前建立直接使用,同时没有预先配置测试所需的lvm环境导致测试失败

- - grep输出由于没有考察RISCV的环境对应输出造成缺陷误判

- - - [os-basic/oe_test_dmraid](https://gitee.com/openeuler/mugen/blob/master/testcases/system-test/system-integration/os-basic/oe_test_dmraid/oe_test_dmraid.sh) ``dmraid -s`` 输出为 ``no block devices found`` ，而测试脚本预期结果为 ``no raid disks`` ，导致没有判定出 raid 不存在
- - - [openssl/oe_test_openssl_DSA_algorithm](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/openssl/oe_test_openssl_DSA_algorithm.sh) ``grep 'BEGIN DSA PRIVATE KEY'`` 失败，实际应为 ``BEGIN PRIVATE KEY`` 。同样的错误影响了 11 个测试用例
- - - [openssl/oe_test_openssl_speed](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/openssl/oe_test_openssl_speed.sh) ``grep "aes-128 cbc"`` 和 ``grep "sm4-cbc"`` 失败，实际应为 ``aes-128-cbc`` 和 ``SM4-CBC``
- - - [iptables/oe_test_iptables-restore_01](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/iptables/oe_test_ip6tables-restore_01.sh) ``grep "DROP       icmp"`` 失败， ``ip6tables -nvL`` 输出没有出现该字段
- - - [iptables/oe_test_ip6tables-save](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/iptables/oe_test_ip6tables-save.sh) ``grep -A 200 nat | grep -A 100 mangle | grep -A 80 raw | grep -A 60 security | grep filter`` ， ``ip6tables-save`` 命令实际输出没有出现这些字段


- - mugen脚本存在一些随着软件更新而出现的兼容性问题：

- - - [kmod/oe_test_insmod-lsmod](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/kmod/oe_test_insmod-lsmod/oe_test_insmod-lsmod.sh) 在 23.09 riscv 的内核上， raid0 模块文件名为 ``raid0.ko.xz`` 、 faulty 模块文件名为 ``faulty.ko.xz`` ，而测试套预期文件名为 ``raid0.ko`` 和 ``faulty.ko`` ，导致测试失败
- - - [os-basic/oe_test_gcc_01](https://gitee.com/openeuler/mugen/blob/master/testcases/system-test/system-integration/os-basic/oe_test_gcc/oe_test_gcc_01.sh) 测试套预期为 ``warning: ‘i’ is used uninitialized in this function`` 但是实际输出
      ```bash
      gcc -Wall main.c -o main
      main.c: In function 'main':
      main.c:6:4: warning: 'i' is used uninitialized [-Wuninitialized]
          6 |    printf("\n The Geek Stuff [%d]\n", i);
            |    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      main.c:5:8: note: 'i' was declared here
          5 |    int i;
            |
      ``

- - - [gsl/oe_test_gsl_histogram_01](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/gsl/oe_test_gsl_histogram_01.sh): 23.09中gsl对应版本为2.7.1，软件命令行使用格式有所改变，但mugen脚本没有更新

- - - [smoke-basic-os/oe_test_aide_init_database](https://gitee.com/openeuler/mugen/blob/master/testcases/smoke-test/smoke-basic-os/oe_test_aide_init_database/oe_test_aide_init_database.sh)中```aide --init```预期输出应该包括"AIDE initialized database at /var/lib/aide/aide.db.new.gz"但是实际输出为：

      ```bash
      Start timestamp: 2023-08-13 19:32:26 - - -0800 (AIDE 0.18.5)
      AIDE successfully initialized database.
      New AIDE database written to /var/lib/aide/aide.db.new.gz

      Number of entries:	51176

      ---------------------------------------------------
      The attributes of the (uncompressed) database(s):
      ---------------------------------------------------

      /var/lib/aide/aide.db.new.gz
      .......
      ```

- - - [smoke-basic-os/oe_test_rsyslog_10](https://gitee.com/openeuler/mugen/blob/master/testcases/smoke-test/smoke-basic-os/oe_test_rsyslog_10/oe_test_rsyslog_10.sh)中date命令的输出按空格分割第六个字符按预期为应为时区，例如```Sun Aug 13 07:34:01 PM CST 2023```但是实际输出为```Sun Aug 13 07:34:01 CST 2023```，输出按空格分割第六个字符变成了年份。

- - mugen脚本与RISC-V架构的兼容性存在问题：

- - - [os-basic/oe_test_awk](https://gitee.com/openeuler/mugen/blob/master/testcases/system-test/system-integration/os-basic/oe_test_awk/oe_test_awk.sh)riscv64 上没 cpuid;riscv架构 /proc/cpuinfo 中对cpu相关的描述与x86不一致，导致检索不到"cpu"关键词。riscv类似的概念叫"hart"。

- - - [os-basic/oe_test_uname](https://gitee.com/openeuler/mugen/blob/master/testcases/system-test/system-integration/os-basic/oe_test_uname/oe_test_uname.sh) ``uname -m | grep -E "aarch64|x86_64"`` 显然在 riscv 上无法通过

- - - [os-basic/oe_test_system_log_dmesg](https://gitee.com/openeuler/mugen/blob/master/testcases/system-test/system-integration/os-basic/oe_test_system_log_dmesg/oe_test_system_log_dmesg.sh)脚本中有`dmesg | grep -iE "Booting Linux on physical CPU|smpboot"`，riscv上没这些信息

- - - [libreswan/oe_test_libreswan_ipsec_auto_2](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/libreswan/oe_test_libreswan_ipsec_auto_2.sh)：RISC-V架构下ipsec auto无“--listgroups"和"--rereadgroups"选项

- - 脚本设计缺陷

- - - [libosinfo/oe_test_osinfo-db-import](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/libosinfo/oe_test_osinfo-db-import/oe_test_osinfo-db-import.sh) 中导出文件名按照当前时间命名，测试脚本中寻找的导出文件名是写死的

- - - [cloud-init/oe_test_service_cloud-final](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/cloud-init/oe_test_service_cloud-final.sh)# 在riscv上，`systemctl disable`命令的输出结果是：Removed "服务名"，而在arm上输出没有这两个双引号，在riscv上测试用例是将双引号也当成了服务名的一部分。systemctl输出不同，应对测试用例进行适配,testcases/cli-test/common/common_lib.sh#L66处symlink_file=后，可增加``eval symlink_file=$symlink_file``去除双引号,其它测试套及用例有的也是因为这一问题失败

- - - [freeradius/oe_test_freeradius_freeradius-utils_radclient2](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/freeradius/oe_test_freeradius_freeradius-utils_radclient2/oe_test_freeradius_freeradius-utils_radclient2.sh)失败的是-r参数，但按https://wiki.freeradius.org/config/Radclient ，-r retries : If timeout, retry sending the packet 'retries' times.就是说重发次数不一定为预设的次数。这里测试用了必须等于作为尺度，应是不可靠的；改为小于等于后测试通过

- - - [freeradius/oe_test_freeradius_freeradius-utils_radlastAndRadsniff](https://gitee.com/openeuler/mugen/blob/master/testcases/cli-test/freeradius/oe_test_freeradius_freeradius-utils_radclient2/oe_test_freeradius_freeradius-utils_radclient2.sh):# 测试条件太脆弱：[ $(radlast | grep -c "oot") -gt $(radlast -t "00:00" | grep -c "oot") ],如果今天0点后没有用户登录行为发生，则测试必失败，因为上述条件用了-gt（大于）来检测比较截止今天0点时的用户登录次数,改成-ge（大于等于）测试通过

- - 目前openEuler-RISCV使用的仍是qemu镜像，其与mugen脚本的兼容性以及与实体机的性能差异造成测试的误判（由上游提供log可知其依然使用qemu进行mugen测试）
- openEuler-RISCV自身存在问题
- - qemu的模拟对测试环境的复现程度的问题
### mugen上游仓库公开的脚本存在一定历史遗留问题
## 合入方案（我方提出+商讨+定案分工）
> Todo:思考合理方案，准备
### 明确合入范围及优先度
- mugen合入范围可分为：
- - 合入进行适配的本不兼容RISC-V架构部分脚本
- - 合入新增的自动创建qemu镜像以及测试后自动分类的python脚本
- - 后续测试从上游拿到远程资源的可能（即测试的同步合入和环境的统一）
- 合入优先度：
- - 合入进行适配的本不兼容RISC-V架构部分脚本 -- 高优先
- - 合入新增的自动创建qemu镜像以及测试后自动分类的python脚本 -- 可选
- - 后续测试从上游拿到远程资源的可能（即测试的同步合入和环境的统一） -- 可选
### 对于目前的脚本成果
- 合入mugen仓库（或许需要将代码规范向mugen/lib中脚本规范靠拢）
- 已经修改过的脚本，判断是否尽量满足三种架构均进行适配的情况，考虑对此进行进一步适配
- 目前已经分析出问题的脚本，考虑做出修改，或与上游商讨修改方案
### 对于目前的问题合入时的商讨
- 上游在qemu中的测试方案与RISCV mugen的测试方案的对比
- - 包括
- - - 测试环境要求
- - - 服务器环境配置
- - - 是否使用CI进行自动配置
- - - 测试流程，log整理，是否为问题的判定（与目前mugen测试存在缺陷相结合）
- - - 测试样例范围限制
- 对于目前上游存在一定问题的仓库，上游的测试应对方案，以及脚本修改涉及的各类问题，商讨解决方案
- 合入方案的商讨
- - 若对仓库中脚本的修改仍的不出结论，应确定合理的测试方针，并再之后共同完善mugen公开出来的仓库
- - 得出结论的商讨合入方案：一次对之前出现问题的做出修改 or 调整测试策略并完善脚本
### 可行方案
- 第一步：
  将mugen目前不兼容RISC-V的脚本修改结果向上游提出议题，合并相关代码（本分支的自动化脚本可选），同时了解上游mugen测试流程，要求，虚拟机和服务器配置方法，并根据自身条件向其靠拢
- 第二步：
  当自身条件可以和上游接近时，提出是否可向上游申请服务器资源进行同步测试，包括同时出镜像同时进行mugen测试，log整理可由测试小队成员负责，要求尽量跟进上游测试步伐
### 合入后的维护方案
- 了解mugen代码的合入，修改方案，尝试对架构相关的提出对应要求