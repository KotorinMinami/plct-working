# OpenKylin 0.9.5 RISCV autopkgtest测试结果及说明
## 测试说明
### 测试框架 autopkgtest
autopkgtest 是运行由DEP8定义的测试套件的软件。其软件的测试套由软件上游编写，并遵循DEP8的规定。
### 测试范围
本次测试扫描了openKylin镜像提供的仓库中所有的软件包共40925个，其中28873个软件在仓库中无源码， 3786个软件在源码中无法解压出测试套，剩余软件为本次测试的讨论及测试范围，其中共872个测试套数，共2030个测试例
### 测试环境
- 测试镜像：openKylin-0.9.5-qemu-riscv64.img ， openkylin-0.9.5-hifive-unmatched-riscv64.img

由于进行测试时openKylin尚未发出适用于qemu的镜像，故使用u-boot在qemu中启动测试对应版本的umatched镜像，由于测试的以软件包为主，故不同镜像内核的差异对测试结果的影响应该在一个可以接受的范围。
- 测试方式：获取镜像中提供的软件仓中的源码，并对其运行`autopkgtest -- qemu`的测试，测试过程中autopkgtest会自动归类错误，备份镜像环境等
- 测试代码获取方式：

在运行autopkgtest时在前面添加--shell字样，即`autopkgtest --shell -- qemu`，其便会在运行测试例的时候暂停并给出访问系统镜像的方法，以及测试源码在guest的位置
- 测试代码（.dsc文件为测试源代码）：
```
autopkgtest pulseaudio_13.99.1-ok10.dsc -o pulseaudio -d -B \
-- qemu -u root -p openkylin \ 
--qemu-architecture=riscv64 -c 8 --ram-size=8192 -d  \ 
--qemu-options='-machine virt -kernel /home/minami/Documents/ukylin/u-boot.bin' \ t.qcow2
```
对应测试时启动的qemu启动参数为
```
qemu-system-riscv64 \
-m 8192 -smp 8 -nographic \
-device virtio-net-device,netdev=usernet \
-netdev user,id=usernet,hostfwd=tcp:127.0.0.1:10022-:22 \
-object rng-random,filename=/dev/urandom,id=rng0 \
-device virtio-rng-pci,rng=rng0,id=rng-device0 \
-monitor unix:/tmp/autopkgtest-qemu.gdputb5i/monitor,server=on,wait=off \
-virtfs local,id=autopkgtest,path=/tmp/autopkgtest-qemu.gdputb5i/shared,security_model=none,mount_tag=autopkgtest \
-device virtio-serial -chardev socket,path=/tmp/autopkgtest-qemu.gdputb5i/hvc0,server=on,wait=off,id=hvc0 \
-device virtconsole,chardev=hvc0 \
-chardev socket,path=/tmp/autopkgtest-qemu.gdputb5i/hvc1,server=on,wait=off,id=hvc1 \
-device virtconsole,chardev=hvc1 \
-serial unix:/tmp/autopkgtest-qemu.gdputb5i/ttyS0,server=on,wait=off \
-drive index=0,file=/tmp/autopkgtest-qemu.gdputb5i/overlay.img,format=qcow2,cache=unsafe,if=virtio,discard=unmap \
-machine virt \
-kernel /home/minami/Documents/ukylin/u-boot.bin
```
- qemu镜像的设置方法，通过插入内核参数以及设置开机自启动，使得qemu有一个串行的console可供autopkgtest进行使用，同时更新了除mount以外的全部预安装软件，并安装了rng-tools以及python3软件包，同时扩容并将镜像格式convert为.qcow
2格式

## 测试结果说明
- 详细结果全表如[result.csv](./result.csv)
- 失败样例及其原因概括如[failureCause.csv](./failureCause.csv)
- 具体的log可参见[test/软件包名](./test/) 对应文件夹中log为运行是总log,summary为简短的总结，testbed-packages罗列了进行测试用到的testbed的软件包安装情况及具体版本，即运行测试的软件环境，testpkg-version文件指出了测试包的版本，其余文件遵循`testname-*`的格式，其中testname为所执行的测试例的名字，而*可以为packages,stdout,stderr，分别代表了样例安装测试的包和依赖，测试时的正常标准输出日志以及错误信息日志。
- 其余无法从源码中获取测试例的软件包详见[emptytest/软件包名](./emptytest/)
- 软件仓中无法获得源码的软件包可见[pkg_no_source](./pkg_no_source)
- log文件解析：

log文件记录了autopkgtest的运行过程，一般为：启动并初始化qemu -> 导入并解析源码包 -> 根据包中的测试例要求配置测试环境，安装软件 -> 进行测试 -> Summary

下以file测试套为例查看测试过程中的记录：
```
autopkgtest [15:53:14]: test run-testsuite: [-----------------------
autopkgtest: DBG: testbed command ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.Cy11qq/build.mlk/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.Cy11qq/run-testsuite-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.Cy11qq/run-testsuite-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.Cy11qq/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.Cy11qq/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; chmod +x /tmp/autopkgtest.Cy11qq/build.mlk/src/debian/tests/run-testsuite; exec /tmp/autopkgtest.Cy11qq/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.Cy11qq/run-testsuite-stderr --stdout=/tmp/autopkgtest.Cy11qq/run-testsuite-stdout -- /tmp/autopkgtest.Cy11qq/build.mlk/src/debian/tests/run-testsuite ;'], kind test, sout raw, serr raw, env []
Testing: CVE-2014-1943.testfile ... pass
Testing: JW07022A.mp3.testfile ... pass
Testing: escapevel.testfile ... pass
Testing: fit-map-data.testfile ... pass
Testing: gedcom.testfile ... pass
Testing: hddrawcopytool.testfile ... pass
Testing: issue311docx.testfile ... pass
Testing: issue359xlsx.testfile ... pass
Testing: json1.testfile ... pass
Testing: json2.testfile ... pass
Testing: json3.testfile ... pass
Testing: regex-eol.testfile ... pass
Testing: zstd-v0.2-FF.testfile ... pass
Testing: zstd-v0.3-FF.testfile ... pass
Testing: zstd-v0.4-FF.testfile ... pass
Testing: zstd-v0.5-FF.testfile ... pass
Testing: zstd-v0.6-FF.testfile ... pass
Testing: zstd-v0.7-21.testfile ... pass
Testing: zstd-v0.7-22.testfile ... pass
Testing: zstd-v0.8-01.testfile ... pass
Testing: zstd-v0.8-02.testfile ... pass
Testing: zstd-v0.8-03.testfile ... pass
Testing: zstd-v0.8-16.testfile ... pass
Testing: zstd-v0.8-20.testfile ... pass
Testing: zstd-v0.8-21.testfile ... pass
Testing: zstd-v0.8-22.testfile ... pass
Testing: zstd-v0.8-23.testfile ... pass
Testing: zstd-v0.8-F4.testfile ... pass
Testing: zstd-v0.8-FF.testfile ... pass
autopkgtest: DBG: testbed command exited with code 0
autopkgtest [15:53:20]: test run-testsuite: -----------------------]
```
可看到测试时其实是对qemu发送了一个执行的信号，然后qemu执行后会将stdout及stderr输出，最后并入总结

## 测试结果
### 结果总体说明
本次测试总共扫描了40925个软件包，其中进行了有效测试的包有872个，测试例共2030个，通过973个，失败1057个，另有3786个软件包为源码包内无测试例，其余则无法从软件仓中获取源码
### 失败结果归类及说明
- FAIL badpkg 
    - 此结果一般出现在配置测试环境时安装测试需要的软件失败的时候。这个结果的出现大多数代表了测试的软件实际上并不支持测试的功能，或者组件不完善的情况。其在log文件的体现一般如下：
```
autopkgtest: DBG: testbed command ['/bin/sh', '-ec', ' apt-get install --assume-yes --fix-broken -o APT::Status-Fd=3 -o APT::Install-Recommends=false -o Dpkg::Options::=--force-confnew -o Debug::pkgProblemResolver=true 3>&2 2>&1'], kind install, sout raw, serr pipe, env ['DEBIAN_FRONTEND=noninteractive', 'APT_LISTBUGS_FRONTEND=none', 'APT_LISTCHANGES_FRONTEND=none']
Reading package lists...
Building dependency tree...
Reading state information...
Correcting dependencies...Starting pkgProblemResolver with broken count: 3
Starting 2 pkgProblemResolver with broken count: 3
Investigating (0) libaprutil1-dev:riscv64 < none -> 1.6.1-ok2 @un uN Ib >
Broken libaprutil1-dev:riscv64 Depends on libapr1-dev:riscv64 < none | 1.7.0-ok1 @un uH >
  Considering libapr1-dev:riscv64 2 as a solution to libaprutil1-dev:riscv64 0
  Holding Back libaprutil1-dev:riscv64 rather than change libapr1-dev:riscv64
Investigating (0) apache2-dev:riscv64 < none -> 2.4.54-ok1 @un uN Ib >
Broken apache2-dev:riscv64 Depends on libapr1-dev:riscv64 < none | 1.7.0-ok1 @un uH >
  Considering libapr1-dev:riscv64 2 as a solution to apache2-dev:riscv64 0
  Holding Back apache2-dev:riscv64 rather than change libapr1-dev:riscv64
Investigating (0) autopkgtest-satdep:riscv64 < 0 @iU mK Nb Ib >
Broken autopkgtest-satdep:riscv64 Depends on apache2-dev:riscv64 < none | 2.4.54-ok1 @un uH >
  Considering apache2-dev:riscv64 0 as a solution to autopkgtest-satdep:riscv64 -2
  Removing autopkgtest-satdep:riscv64 rather than change apache2-dev:riscv64
Done
 Done
Starting pkgProblemResolver with broken count: 0
Starting 2 pkgProblemResolver with broken count: 0
Done
The following packages were automatically installed and are no longer required:
  libdjvulibre-text libdjvulibre21 libegl-dev libgl-dev libglu1-mesa-dev
  libglx-dev libmpdec2 libvulkan-dev libx11-dev libxau-dev libxcb1-dev
  libxdmcp-dev libxext-dev qt5-qmake qt5-qmake-bin x11proto-core-dev
  x11proto-dev xorg-sgml-doctools xtrans-dev
Use 'apt autoremove' to remove them.
The following additional packages will be installed:
  autoconf automake autopoint autotools-dev build-essential g++ g++-9 gcc
  gcc-9 libbytes-random-secure-perl libcc1-0 libcrypt-random-seed-perl
  libcrypt-ssleay-perl libencode-locale-perl libfile-listing-perl
  libhtml-parser-perl libhtml-tagset-perl libhtml-tree-perl
  libhttp-cookies-perl libhttp-date-perl libhttp-message-perl
  libhttp-negotiate-perl libio-html-perl libio-socket-ssl-perl
  liblwp-mediatypes-perl liblwp-protocol-https-perl libmath-random-isaac-perl
  libnet-http-perl libnet-ssleay-perl libsigsegv2 libtimedate-perl libtool
  libtry-tiny-perl libwww-perl libwww-robotrules-perl m4 perl-doc
  perl-openssl-defaults
Suggested packages:
  autoconf-archive gnu-standards autoconf-doc gcc-9-doc bison flex gcc-doc
  gcc-multilib gdb manpages-dev gcc-9-locales libdata-dump-perl libtool-doc
  gfortran | fortran95-compiler gcj-jdk libsub-name-perl libauthen-ntlm-perl
  m4-doc
Recommended packages:
  libhtml-format-perl libclone-perl libmath-random-isaac-xs-perl libltdl-dev
  libdata-dump-perl libhtml-form-perl libhttp-daemon-perl libmailtools-perl
The following packages will be REMOVED:
  autopkgtest-satdep
The following NEW packages will be installed:
  autoconf automake autopoint autotools-dev build-essential g++ g++-9 gcc
  gcc-9 libbytes-random-secure-perl libcc1-0 libcrypt-random-seed-perl
  libcrypt-ssleay-perl libencode-locale-perl libfile-listing-perl
  libhtml-parser-perl libhtml-tagset-perl libhtml-tree-perl
  libhttp-cookies-perl libhttp-date-perl libhttp-message-perl
  libhttp-negotiate-perl libio-html-perl libio-socket-ssl-perl
  liblwp-mediatypes-perl liblwp-protocol-https-perl libmath-random-isaac-perl
  libnet-http-perl libnet-ssleay-perl libsigsegv2 libtimedate-perl libtool
  libtry-tiny-perl libwww-perl libwww-robotrules-perl m4 perl-doc
  perl-openssl-defaults
0 upgraded, 38 newly installed, 1 to remove and 18 not upgraded.
1 not fully installed or removed.
Need to get 25.6 MB of archives.
After this operation, 60.2 MB of additional disk space will be used.
Ign:1 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libsigsegv2 riscv64 2.12-ok1
Ign:2 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 m4 riscv64 1.4.18-ok2
Ign:3 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 autoconf all 2.71-ok2
Get:4 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 autotools-dev all 20220506-ok1 [41.6 kB]
Get:5 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 automake all 1:1.16.5-ok1 [557 kB]
Get:6 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 autopoint all 0.19.8.1-ok1 [410 kB]
Get:7 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libcc1-0 riscv64 10-20200411-ok5 [42.3 kB]
Get:8 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 gcc-9 riscv64 9.3.0-ok4 [7,417 kB]
Get:9 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 gcc riscv64 4:9.3.0-ok7 [5,160 B]
Get:10 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 g++-9 riscv64 9.3.0-ok4 [7,571 kB]
Get:11 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 g++ riscv64 4:9.3.0-ok7 [1,470 B]
Get:12 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 build-essential riscv64 12.8-ok1 [4,000 B]
Get:13 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libcrypt-random-seed-perl all 0.03-ok2 [20.3 kB]
Get:14 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libmath-random-isaac-perl all 1.004-ok2 [18.9 kB]
Get:15 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libbytes-random-secure-perl all 0.29-ok2 [26.7 kB]
Get:16 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 perl-openssl-defaults riscv64 5-ok1 [6,742 B]
Get:17 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libcrypt-ssleay-perl riscv64 0.73.06-ok2 [44.9 kB]
Get:18 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libencode-locale-perl all 1.05-ok2 [11.1 kB]
Get:19 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libtimedate-perl all 2.3300-ok2 [33.5 kB]
Get:20 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhttp-date-perl all 6.05-ok3 [15.9 kB]
Get:21 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libfile-listing-perl all 6.15-ok2 [17.0 kB]
Get:22 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhtml-tagset-perl all 3.20-ok2 [11.0 kB]
Get:23 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhtml-parser-perl riscv64 3.76-ok1 [85.2 kB]
Get:24 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhtml-tree-perl all 5.07-ok2 [199 kB]
Get:25 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libio-html-perl all 1.004-ok2 [20.3 kB]
Get:26 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 liblwp-mediatypes-perl all 6.04-ok2 [19.7 kB]
Get:27 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhttp-message-perl all 6.36-ok1 [76.3 kB]
Get:28 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhttp-cookies-perl all 6.10-ok1 [17.5 kB]
Get:29 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libhttp-negotiate-perl all 6.01-ok2 [12.0 kB]
Get:30 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libnet-ssleay-perl riscv64 1.88-ok2 [296 kB]
Get:31 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libio-socket-ssl-perl all 2.075-ok2 [191 kB]
Get:32 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libnet-http-perl all 6.22-ok2 [28.1 kB]
Get:33 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libtry-tiny-perl all 0.31-ok1 [20.5 kB]
Get:34 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libwww-robotrules-perl all 6.02-ok2 [12.3 kB]
Get:35 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libwww-perl all 6.43-ok2 [140 kB]
Get:36 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 liblwp-protocol-https-perl all 6.10-ok1 [8,848 B]
Get:37 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libtool all 2.4.6-ok1 [159 kB]
Get:38 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 perl-doc all 5.30.0-ok3 [7,508 kB]
Get:1 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 libsigsegv2 riscv64 2.12-ok1 [11.5 kB]
Get:2 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 m4 riscv64 1.4.18-ok2 [191 kB]
Get:3 http://archive.build.openkylin.top/openkylin yangtze/main riscv64 autoconf all 2.71-ok2 [390 kB]
Fetched 25.6 MB in 1min 19s (326 kB/s)
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 161111 files and directories currently installed.)
Removing autopkgtest-satdep (0) ...
Selecting previously unselected package libsigsegv2:riscv64.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 161111 files and directories currently installed.)
Preparing to unpack .../00-libsigsegv2_2.12-ok1_riscv64.deb ...
Unpacking libsigsegv2:riscv64 (2.12-ok1) ...
Selecting previously unselected package m4.
Preparing to unpack .../01-m4_1.4.18-ok2_riscv64.deb ...
Unpacking m4 (1.4.18-ok2) ...
Selecting previously unselected package autoconf.
Preparing to unpack .../02-autoconf_2.71-ok2_all.deb ...
Unpacking autoconf (2.71-ok2) ...
Selecting previously unselected package autotools-dev.
Preparing to unpack .../03-autotools-dev_20220506-ok1_all.deb ...
Unpacking autotools-dev (20220506-ok1) ...
Selecting previously unselected package automake.
Preparing to unpack .../04-automake_1%3a1.16.5-ok1_all.deb ...
Unpacking automake (1:1.16.5-ok1) ...
Selecting previously unselected package autopoint.
Preparing to unpack .../05-autopoint_0.19.8.1-ok1_all.deb ...
Unpacking autopoint (0.19.8.1-ok1) ...
Selecting previously unselected package libcc1-0:riscv64.
Preparing to unpack .../06-libcc1-0_10-20200411-ok5_riscv64.deb ...
Unpacking libcc1-0:riscv64 (10-20200411-ok5) ...
Selecting previously unselected package gcc-9.
Preparing to unpack .../07-gcc-9_9.3.0-ok4_riscv64.deb ...
Unpacking gcc-9 (9.3.0-ok4) ...
Selecting previously unselected package gcc.
Preparing to unpack .../08-gcc_4%3a9.3.0-ok7_riscv64.deb ...
Unpacking gcc (4:9.3.0-ok7) ...
Selecting previously unselected package g++-9.
Preparing to unpack .../09-g++-9_9.3.0-ok4_riscv64.deb ...
Unpacking g++-9 (9.3.0-ok4) ...
Selecting previously unselected package g++.
Preparing to unpack .../10-g++_4%3a9.3.0-ok7_riscv64.deb ...
Unpacking g++ (4:9.3.0-ok7) ...
Selecting previously unselected package build-essential.
Preparing to unpack .../11-build-essential_12.8-ok1_riscv64.deb ...
Unpacking build-essential (12.8-ok1) ...
Selecting previously unselected package libcrypt-random-seed-perl.
Preparing to unpack .../12-libcrypt-random-seed-perl_0.03-ok2_all.deb ...
Unpacking libcrypt-random-seed-perl (0.03-ok2) ...
Selecting previously unselected package libmath-random-isaac-perl.
Preparing to unpack .../13-libmath-random-isaac-perl_1.004-ok2_all.deb ...
Unpacking libmath-random-isaac-perl (1.004-ok2) ...
Selecting previously unselected package libbytes-random-secure-perl.
Preparing to unpack .../14-libbytes-random-secure-perl_0.29-ok2_all.deb ...
Unpacking libbytes-random-secure-perl (0.29-ok2) ...
Selecting previously unselected package perl-openssl-defaults:riscv64.
Preparing to unpack .../15-perl-openssl-defaults_5-ok1_riscv64.deb ...
Unpacking perl-openssl-defaults:riscv64 (5-ok1) ...
Selecting previously unselected package libcrypt-ssleay-perl.
Preparing to unpack .../16-libcrypt-ssleay-perl_0.73.06-ok2_riscv64.deb ...
Unpacking libcrypt-ssleay-perl (0.73.06-ok2) ...
Selecting previously unselected package libencode-locale-perl.
Preparing to unpack .../17-libencode-locale-perl_1.05-ok2_all.deb ...
Unpacking libencode-locale-perl (1.05-ok2) ...
Selecting previously unselected package libtimedate-perl.
Preparing to unpack .../18-libtimedate-perl_2.3300-ok2_all.deb ...
Unpacking libtimedate-perl (2.3300-ok2) ...
Selecting previously unselected package libhttp-date-perl.
Preparing to unpack .../19-libhttp-date-perl_6.05-ok3_all.deb ...
Unpacking libhttp-date-perl (6.05-ok3) ...
Selecting previously unselected package libfile-listing-perl.
Preparing to unpack .../20-libfile-listing-perl_6.15-ok2_all.deb ...
Unpacking libfile-listing-perl (6.15-ok2) ...
Selecting previously unselected package libhtml-tagset-perl.
Preparing to unpack .../21-libhtml-tagset-perl_3.20-ok2_all.deb ...
Unpacking libhtml-tagset-perl (3.20-ok2) ...
Selecting previously unselected package libhtml-parser-perl:riscv64.
Preparing to unpack .../22-libhtml-parser-perl_3.76-ok1_riscv64.deb ...
Unpacking libhtml-parser-perl:riscv64 (3.76-ok1) ...
Selecting previously unselected package libhtml-tree-perl.
Preparing to unpack .../23-libhtml-tree-perl_5.07-ok2_all.deb ...
Unpacking libhtml-tree-perl (5.07-ok2) ...
Selecting previously unselected package libio-html-perl.
Preparing to unpack .../24-libio-html-perl_1.004-ok2_all.deb ...
Unpacking libio-html-perl (1.004-ok2) ...
Selecting previously unselected package liblwp-mediatypes-perl.
Preparing to unpack .../25-liblwp-mediatypes-perl_6.04-ok2_all.deb ...
Unpacking liblwp-mediatypes-perl (6.04-ok2) ...
Selecting previously unselected package libhttp-message-perl.
Preparing to unpack .../26-libhttp-message-perl_6.36-ok1_all.deb ...
Unpacking libhttp-message-perl (6.36-ok1) ...
Selecting previously unselected package libhttp-cookies-perl.
Preparing to unpack .../27-libhttp-cookies-perl_6.10-ok1_all.deb ...
Unpacking libhttp-cookies-perl (6.10-ok1) ...
Selecting previously unselected package libhttp-negotiate-perl.
Preparing to unpack .../28-libhttp-negotiate-perl_6.01-ok2_all.deb ...
Unpacking libhttp-negotiate-perl (6.01-ok2) ...
Selecting previously unselected package libnet-ssleay-perl.
Preparing to unpack .../29-libnet-ssleay-perl_1.88-ok2_riscv64.deb ...
Unpacking libnet-ssleay-perl (1.88-ok2) ...
Selecting previously unselected package libio-socket-ssl-perl.
Preparing to unpack .../30-libio-socket-ssl-perl_2.075-ok2_all.deb ...
Unpacking libio-socket-ssl-perl (2.075-ok2) ...
Selecting previously unselected package libnet-http-perl.
Preparing to unpack .../31-libnet-http-perl_6.22-ok2_all.deb ...
Unpacking libnet-http-perl (6.22-ok2) ...
Selecting previously unselected package libtry-tiny-perl.
Preparing to unpack .../32-libtry-tiny-perl_0.31-ok1_all.deb ...
Unpacking libtry-tiny-perl (0.31-ok1) ...
Selecting previously unselected package libwww-robotrules-perl.
Preparing to unpack .../33-libwww-robotrules-perl_6.02-ok2_all.deb ...
Unpacking libwww-robotrules-perl (6.02-ok2) ...
Selecting previously unselected package libwww-perl.
Preparing to unpack .../34-libwww-perl_6.43-ok2_all.deb ...
Unpacking libwww-perl (6.43-ok2) ...
Selecting previously unselected package liblwp-protocol-https-perl.
Preparing to unpack .../35-liblwp-protocol-https-perl_6.10-ok1_all.deb ...
Unpacking liblwp-protocol-https-perl (6.10-ok1) ...
Selecting previously unselected package libtool.
Preparing to unpack .../36-libtool_2.4.6-ok1_all.deb ...
Unpacking libtool (2.4.6-ok1) ...
Selecting previously unselected package perl-doc.
Preparing to unpack .../37-perl-doc_5.30.0-ok3_all.deb ...
Adding 'diversion of /usr/bin/perldoc to /usr/bin/perldoc.stub by perl-doc'
Unpacking perl-doc (5.30.0-ok3) ...
Setting up libmath-random-isaac-perl (1.004-ok2) ...
Setting up libhtml-tagset-perl (3.20-ok2) ...
Setting up liblwp-mediatypes-perl (6.04-ok2) ...
Setting up libtry-tiny-perl (0.31-ok1) ...
Setting up perl-openssl-defaults:riscv64 (5-ok1) ...
Setting up perl-doc (5.30.0-ok3) ...
Setting up libnet-http-perl (6.22-ok2) ...
Setting up libencode-locale-perl (1.05-ok2) ...
Setting up autotools-dev (20220506-ok1) ...
Setting up libcrypt-random-seed-perl (0.03-ok2) ...
Setting up libsigsegv2:riscv64 (2.12-ok1) ...
Setting up libio-html-perl (1.004-ok2) ...
Setting up autopoint (0.19.8.1-ok1) ...
Setting up libtimedate-perl (2.3300-ok2) ...
Setting up libwww-robotrules-perl (6.02-ok2) ...
Setting up libhtml-parser-perl:riscv64 (3.76-ok1) ...
Setting up libcc1-0:riscv64 (10-20200411-ok5) ...
Setting up libnet-ssleay-perl (1.88-ok2) ...
Setting up gcc-9 (9.3.0-ok4) ...
Setting up libhttp-date-perl (6.05-ok3) ...
Setting up libfile-listing-perl (6.15-ok2) ...
Setting up libtool (2.4.6-ok1) ...
Setting up libhtml-tree-perl (5.07-ok2) ...
Setting up m4 (1.4.18-ok2) ...
Setting up gcc (4:9.3.0-ok7) ...
Setting up libbytes-random-secure-perl (0.29-ok2) ...
Setting up g++-9 (9.3.0-ok4) ...
Setting up autoconf (2.71-ok2) ...
Setting up g++ (4:9.3.0-ok7) ...
update-alternatives: using /usr/bin/g++ to provide /usr/bin/c++ (c++) in auto mode
Setting up libcrypt-ssleay-perl (0.73.06-ok2) ...
Setting up build-essential (12.8-ok1) ...
Setting up libio-socket-ssl-perl (2.075-ok2) ...
Setting up libhttp-message-perl (6.36-ok1) ...
Setting up automake (1:1.16.5-ok1) ...
update-alternatives: using /usr/bin/automake-1.16 to provide /usr/bin/automake (automake) in auto mode
Setting up libhttp-negotiate-perl (6.01-ok2) ...
Setting up libhttp-cookies-perl (6.10-ok1) ...
Setting up libwww-perl (6.43-ok2) ...
Setting up liblwp-protocol-https-perl (6.10-ok1) ...
Processing triggers for libc-bin (2.36-ok2) ...
Processing triggers for man-db (2.9.1-ok3) ...
Processing triggers for install-info (6.7.0.dfsg.2-ok1) ...
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status}', 'apache2'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status} ${Provides}\n', '*'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: WARNING: package apache2 is not installed though it should be
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status}', 'apache2-dev'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status} ${Provides}\n', '*'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: WARNING: package apache2-dev is not installed though it should be
autopkgtest: DBG: testbed command ['dpkg', '--status', 'autopkgtest-satdep'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: WARNING: Test dependencies are unsatisfiable - calling apt install on test deps directly for further data about failing dependencies in test logs
autopkgtest: DBG: testbed command ['/bin/sh', '-ec', ' apt-get install --assume-yes --simulate build-essential apache2 apache2-dev libwww-perl libnet-ssleay-perl libanyevent-perl libdatetime-perl libhtml-parser-perl libtime-hires-perl libcrypt-ssleay-perl libhttp-dav-perl libprotocol-http2-perl libfcgi-perl libpcre2-dev perl-doc -o APT::Status-Fd=3 -o APT::Install-Recommends=false -o Dpkg::Options::=--force-confnew -o Debug::pkgProblemResolver=true 3>&2 2>&1'], kind install, sout raw, serr pipe, env ['DEBIAN_FRONTEND=noninteractive', 'APT_LISTBUGS_FRONTEND=none', 'APT_LISTCHANGES_FRONTEND=none']
Reading package lists...
Building dependency tree...
Reading state information...
E: Unable to locate package libprotocol-http2-perl
autopkgtest: DBG: testbed command exited with code 100
autopkgtest: DBG: BadPackageError Test dependencies are unsatisfiable. A common reason is that your testbed is out of date with respect to the archive, and you need to use a current testbed or run apt-get update or use -U.
run-test-suite       FAIL badpkg
blame: /home/minami/Documents/openkylin-riscv/src/apache2_2.4.54-ok1.dsc
badpkg: Test dependencies are unsatisfiable. A common reason is that your testbed is out of date with respect to the archive, and you need to use a current testbed or run apt-get update or use -U.
```
- SKIP installation fails and skip-not-installable set
    - 此信息与上条信息类似，但不同的是在归类中这种test被归类为如果依赖及软件无法正常安装的话就跳过这个测试例，其信息形如下：
```
autopkgtest: DBG: testbed command ['/bin/sh', '-ec', ' apt-get install --assume-yes --fix-broken -o APT::Status-Fd=3 -o APT::Install-Recommends=false -o Dpkg::Options::=--force-confnew -o Debug::pkgProblemResolver=true 3>&2 2>&1'], kind install, sout raw, serr pipe, env ['DEBIAN_FRONTEND=noninteractive', 'APT_LISTBUGS_FRONTEND=none', 'APT_LISTCHANGES_FRONTEND=none']
Reading package lists...
Building dependency tree...
Reading state information...
Correcting dependencies...Starting pkgProblemResolver with broken count: 1
Starting 2 pkgProblemResolver with broken count: 1
Investigating (0) autopkgtest-satdep:riscv64 < 0 @iU mK Nb Ib >
Broken autopkgtest-satdep:riscv64 Depends on wine32:riscv64 < none @un H >
  Removing autopkgtest-satdep:riscv64 because I can't find wine32:riscv64
Done
 Done
Starting pkgProblemResolver with broken count: 0
Starting 2 pkgProblemResolver with broken count: 0
Done
The following packages were automatically installed and are no longer required:
  libdjvulibre-text libdjvulibre21 libegl-dev libgl-dev libglu1-mesa-dev
  libglx-dev libmpdec2 libvulkan-dev libx11-dev libxau-dev libxcb1-dev
  libxdmcp-dev libxext-dev qt5-qmake qt5-qmake-bin x11proto-core-dev
  x11proto-dev xorg-sgml-doctools xtrans-dev
Use 'apt autoremove' to remove them.
The following packages will be REMOVED:
  autopkgtest-satdep
0 upgraded, 0 newly installed, 1 to remove and 18 not upgraded.
1 not fully installed or removed.
After this operation, 0 B of additional disk space will be used.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 161111 files and directories currently installed.)
Removing autopkgtest-satdep (0) ...
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status}', 'gpgrt-tools'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status} ${Provides}\n', '*'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: WARNING: package gpgrt-tools is not installed though it should be
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status}', 'libgpg-error-mingw-w64-dev'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status} ${Provides}\n', '*'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: WARNING: package libgpg-error-mingw-w64-dev is not installed though it should be
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status}', 'libgpg-error-dev'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: DBG: testbed command ['dpkg-query', '--show', '-f', '${Status} ${Provides}\n', '*'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 0
autopkgtest: WARNING: package libgpg-error-dev is not installed though it should be
autopkgtest: DBG: testbed command ['dpkg', '--status', 'autopkgtest-satdep'], kind short, sout pipe, serr pipe, env []
autopkgtest: DBG: testbed command exited with code 1
autopkgtest: WARNING: Test dependencies are unsatisfiable - calling apt install on test deps directly for further data about failing dependencies in test logs
autopkgtest: DBG: testbed command ['/bin/sh', '-ec', ' apt-get install --assume-yes --simulate gpgrt-tools libgpg-error-mingw-w64-dev wine32 libgpg-error-dev gcc-mingw-w64-i686 pkg-config -o APT::Status-Fd=3 -o APT::Install-Recommends=false -o Dpkg::Options::=--force-confnew -o Debug::pkgProblemResolver=true 3>&2 2>&1'], kind install, sout raw, serr pipe, env ['DEBIAN_FRONTEND=noninteractive', 'APT_LISTBUGS_FRONTEND=none', 'APT_LISTCHANGES_FRONTEND=none']
Reading package lists...
Building dependency tree...
Reading state information...
Package wine32 is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

E: Package 'wine32' has no installation candidate
E: Unable to locate package gcc-mingw-w64-i686
autopkgtest: DBG: testbed command exited with code 100
autopkgtest: DBG: BadPackageError Test dependencies are unsatisfiable. A common reason is that your testbed is out of date with respect to the archive, and you need to use a current testbed or run apt-get update or use -U.
win32                SKIP installation fails and skip-not-installable set
```
- SKIP Test lists explicitly supported architectures, but the current architecture riscv64 isn't listed
    - 此提示指出此测试并不支持对应的架构，其输出形如下：
```
autopkgtest: DBG: processing dependency @
autopkgtest: DBG: synthesised dependency libcub-dev
autopkgtest: DBG: processing dependency cmake
autopkgtest: DBG: processing dependency make
autopkgtest: DBG: processing dependency nvidia-cuda-toolkit-gcc
compile_testsuite_cuda-g++_C++17 SKIP Test lists explicitly supported architectures, but the current architecture riscv64 isn't listed.
```
- SKIP exit status 77 and marked as skippable
    - 此信息表示测试执行后返回非零值77，且此测试例被标记为可跳过，故跳过，其在log中一般体现为：
```
autopkgtest [02:56:05]: test gdbm: [-----------------------
autopkgtest: DBG: testbed command ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.ZGUy97/build.JWK/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.ZGUy97/gdbm-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.ZGUy97/gdbm-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.ZGUy97/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.ZGUy97/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; chmod +x /tmp/autopkgtest.ZGUy97/build.JWK/src/debian/tests/gdbm; exec /tmp/autopkgtest.ZGUy97/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.ZGUy97/gdbm-stderr --stdout=/tmp/autopkgtest.ZGUy97/gdbm-stdout -- /tmp/autopkgtest.ZGUy97/build.JWK/src/debian/tests/gdbm ;'], kind test, sout raw, serr raw, env []
autopkgtest: DBG: testbed command exited with code 77
autopkgtest [02:56:08]: test gdbm: -----------------------]
autopkgtest: DBG: testbed executing test finished with exit status 77
```
- FAIL non-zero exit status...
    - 省略号后一般为数字，此信息指名了在运行对应测试例的时候返回了非零值，故认为失败在log一般表现为
```
autopkgtest [18:12:28]: test autodep8-python3: [-----------------------
autopkgtest: DBG: testbed command ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.AVSoQ5/build.9vK/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.AVSoQ5/autodep8-python3-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.AVSoQ5/autodep8-python3-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.AVSoQ5/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.AVSoQ5/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; exec /tmp/autopkgtest.AVSoQ5/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.AVSoQ5/autodep8-python3-stderr --stdout=/tmp/autopkgtest.AVSoQ5/autodep8-python3-stdout -- bash -ec \'set -e ; for py in $(py3versions -r 2>/dev/null) ; do cd "$AUTOPKGTEST_TMP" ; echo "Testing with $py:" ; $py -c "import mediainfodll; print(mediainfodll)" ; done\' ;'], kind test, sout raw, serr raw, env []
Testing with python3.8:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'mediainfodll'
autopkgtest: DBG: testbed command exited with code 1
autopkgtest [18:12:34]: test autodep8-python3: -----------------------]
autopkgtest: DBG: testbed executing test finished with exit status 1
```
- FAIL stderr:......
    - 此信息的出现证明测试例输出含有stderr且在定义测试时并不允许stderr的出现，log过程形式大致如下：
```
autopkgtest [22:34:35]: test command1: [-----------------------
autopkgtest: DBG: testbed command ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.ktUJQB/build.qte/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.ktUJQB/command1-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.ktUJQB/command1-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.ktUJQB/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.ktUJQB/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; exec /tmp/autopkgtest.ktUJQB/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.ktUJQB/command1-stderr --stdout=/tmp/autopkgtest.ktUJQB/command1-stdout -- bash -ec \'sed -i "s|^\\(.*\\)GDISK_BIN=./\\(.*\\)|\\\\1GDISK_BIN=/sbin/\\\\2|" ./gdisk_test.sh && ./gdisk_test.sh\' ;'], kind test, sout raw, serr raw, env []
tr: write error: Broken pipe
tr: write error
[0;32m**SUCCESS**[m Temp disk sucessfully created

[0;34m**Testing gdisk binary**[m

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: not present
  BSD: not present
  APM: not present
  GPT: not present

Creating new GPT entries in memory.

Command (? for help): This option deletes all partitions and creates a new protective MBR.
Proceed? (Y/N): 
Command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Create new empty GPT table

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): Partition number (1-128, default 1): First sector (34-131038, default = 2048) or {+-}size{KMGTP}: Last sector (2048-131038, default = 131038) or {+-}size{KMGTP}: Current type is 8300 (Linux filesystem)
Hex code or GUID (L to show codes, Enter = 8300): Changed type of partition to 'Linux filesystem'

Command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Create new partition

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): Using 1
Enter name: 
Command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Change partition 1 name (Linux filesystem -> gkitMIIt)

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): Using 1
Current type is 8300 (Linux filesystem)
Hex code or GUID (L to show codes, Enter = 8300): Changed type of partition to 'Linux swap'

Command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Change partition 1 type (8300 -> 8200)

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): Enter backup filename to save: The operation has completed successfully.

Command (? for help): 
[0;32m**SUCCESS**[m GPT data backuped sucessfully
GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): Using 1

Command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Delete partition 1

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): 
Recovery/transformation command (? for help): b	use backup GPT header (rebuilding main)
c	load backup partition table from disk (rebuilding main)
d	use main GPT header (rebuilding backup)
e	load main partition table from disk (rebuilding backup)
f	load MBR and build fresh GPT from it
g	convert GPT into MBR and exit
h	make hybrid MBR
i	show detailed information on a partition
l	load partition data from a backup file
m	return to main menu
o	print protective MBR data
p	print the partition table
q	quit without saving changes
t	transform BSD disklabel partition
v	verify disk
w	write table to disk and exit
x	extra functionality (experts only)
?	print this menu

Recovery/transformation command (? for help): Enter backup filename to load: 
Recovery/transformation command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Restore the GPT backup

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): 
Expert command (? for help): Enter the disk's unique GUID ('R' to randomize): The new disk GUID is 2847AF5E-A29F-4666-BFA3-1545E1965709

Expert command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m GUID of disk has been sucessfully changed
GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): 
Expert command (? for help): About to wipe out GPT on /tmp/tmp.kFBzNlYiKw. Proceed? (Y/N): Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
GPT data structures destroyed! You may now partition the disk using fdisk or
other utilities.
Blank out MBR? (Y/N): [0;32m**SUCCESS**[m Wipe GPT table

Creating new GPT entries in memory.
[0;32m**SUCCESS**[m EOF successfully exit gdisk

[0;34m**Testing sgdisk binary**[m

Creating new GPT entries in memory.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Create new empty GPT table

Setting name!
partNum is 0
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Create new partition

Setting name!
partNum is 0
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Change partition 1 name (Linux filesystem -> gkitMIIt)

Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Change partition 1 type (8300 -> 8200)

The operation has completed successfully.
[0;32m**SUCCESS**[m GPT data backuped sucessfully
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Delete partition 1

GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): 
Recovery/transformation command (? for help): b	use backup GPT header (rebuilding main)
c	load backup partition table from disk (rebuilding main)
d	use main GPT header (rebuilding backup)
e	load main partition table from disk (rebuilding backup)
f	load MBR and build fresh GPT from it
g	convert GPT into MBR and exit
h	make hybrid MBR
i	show detailed information on a partition
l	load partition data from a backup file
m	return to main menu
o	print protective MBR data
p	print the partition table
q	quit without saving changes
t	transform BSD disklabel partition
v	verify disk
w	write table to disk and exit
x	extra functionality (experts only)
?	print this menu

Recovery/transformation command (? for help): Enter backup filename to load: 
Recovery/transformation command (? for help): 
Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): OK; writing new GUID partition table (GPT) to /tmp/tmp.kFBzNlYiKw.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m Restore the GPT backup

Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
[0;32m**SUCCESS**[m GUID of disk has been sucessfully changed
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
GPT data structures destroyed! You may now partition the disk using fdisk or
other utilities.
[0;32m**SUCCESS**[m Wipe GPT table

Creating new GPT entries in memory.
[0;32m**SUCCESS**[m EOF successfully exit gdisk
autopkgtest: DBG: testbed command exited with code 0
autopkgtest [22:35:05]: test command1: -----------------------]
autopkgtest: DBG: testbed executing test finished with exit status 0
autopkgtest: DBG: sending command to testbed: copyup /tmp/autopkgtest.ktUJQB/command1-stdout /home/minami/Documents/openkylin-riscv/test/gdisk/command1-stdout
autopkgtest-virt-qemu: DBG: executing copyup /tmp/autopkgtest.ktUJQB/command1-stdout /home/minami/Documents/openkylin-riscv/test/gdisk/command1-stdout
autopkgtest-virt-qemu: DBG: ['cmdls', "(['/tmp/autopkgtest-qemu.ebdbfs5z/runcmd', 'sh', '-ec', 'cat </tmp/autopkgtest.ktUJQB/command1-stdout'], ['cat'])"]
autopkgtest-virt-qemu: DBG: ['srcstdin', "<_io.BufferedReader name='/dev/null'>", 'deststdout', "<_io.BufferedWriter name='/home/minami/Documents/openkylin-riscv/test/gdisk/command1-stdout'>", 'devnull_read', <_io.BufferedReader name='/dev/null'>]
autopkgtest-virt-qemu: DBG:  +< /tmp/autopkgtest-qemu.ebdbfs5z/runcmd sh -ec cat </tmp/autopkgtest.ktUJQB/command1-stdout
autopkgtest-virt-qemu: DBG:  +> cat
autopkgtest-virt-qemu: DBG:  +>?
autopkgtest-virt-qemu: DBG:  +<?
autopkgtest: DBG: got reply from testbed: ok
autopkgtest: DBG: sending command to testbed: copyup /tmp/autopkgtest.ktUJQB/command1-stderr /home/minami/Documents/openkylin-riscv/test/gdisk/command1-stderr
autopkgtest-virt-qemu: DBG: executing copyup /tmp/autopkgtest.ktUJQB/command1-stderr /home/minami/Documents/openkylin-riscv/test/gdisk/command1-stderr
autopkgtest-virt-qemu: DBG: ['cmdls', "(['/tmp/autopkgtest-qemu.ebdbfs5z/runcmd', 'sh', '-ec', 'cat </tmp/autopkgtest.ktUJQB/command1-stderr'], ['cat'])"]
autopkgtest-virt-qemu: DBG: ['srcstdin', "<_io.BufferedReader name='/dev/null'>", 'deststdout', "<_io.BufferedWriter name='/home/minami/Documents/openkylin-riscv/test/gdisk/command1-stderr'>", 'devnull_read', <_io.BufferedReader name='/dev/null'>]
autopkgtest-virt-qemu: DBG:  +< /tmp/autopkgtest-qemu.ebdbfs5z/runcmd sh -ec cat </tmp/autopkgtest.ktUJQB/command1-stderr
autopkgtest-virt-qemu: DBG:  +> cat
autopkgtest-virt-qemu: DBG:  +>?
autopkgtest-virt-qemu: DBG:  +<?
autopkgtest: DBG: got reply from testbed: ok
autopkgtest [22:35:06]: test command1:  - - - - - - - - - - results - - - - - - - - - -
command1             FAIL stderr: tr: write error: Broken pipe
autopkgtest [22:35:06]: test command1:  - - - - - - - - - - stderr - - - - - - - - - -
tr: write error: Broken pipe
tr: write error
```
- FLAKY time out
    - 样例超时
```
autopkgtest [18:42:34]: test command2: debian/tests/upstream-testsuite CPP
autopkgtest [18:42:34]: test command2: [-----------------------
autopkgtest: DBG: testbed command ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.tj8Hfd/build.8xK/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; exec /tmp/autopkgtest.tj8Hfd/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.tj8Hfd/command2-stderr --stdout=/tmp/autopkgtest.tj8Hfd/command2-stdout -- bash -ec \'debian/tests/upstream-testsuite CPP\' ;'], kind test, sout raw, serr raw, env []
+ cmake -S . -B /tmp/autopkgtest.tj8Hfd/autopkgtest_tmp -DTHRUST_ENABLE_MULTICONFIG=ON -DTHRUST_MULTICONFIG_ENABLE_DIALECT_CPP11=OFF -DTHRUST_MULTICONFIG_ENABLE_DIALECT_CPP14=ON -DTHRUST_MULTICONFIG_ENABLE_DIALECT_CPP17=ON -DTHRUST_MULTICONFIG_ENABLE_SYSTEM_CPP=ON -DTHRUST_MULTICONFIG_ENABLE_SYSTEM_CUDA=OFF -DTHRUST_MULTICONFIG_ENABLE_SYSTEM_TBB=ON -DTHRUST_MULTICONFIG_ENABLE_SYSTEM_OMP=ON -DTHRUST_MULTICONFIG_WORKLOAD=LARGE -DTHRUST_DEVICE_SYSTEM_OPTIONS=CPP -D_THRUST_CMAKE_DIR=/usr/share/cmake/thrust -Wno-dev
-- The CXX compiler identification is GNU 9.3.0
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found OpenMP_CXX: -fopenmp (found version "4.5") 
-- Found OpenMP: TRUE (found version "4.5") found components: CXX 
-- Found Thrust: /tmp/autopkgtest.tj8Hfd/build.8xK/src/thrust/cmake/thrust-config.cmake (found version "1.15.0.0") 
-- Performing Test CXX_FLAG__Werror
-- Performing Test CXX_FLAG__Werror - Success
-- Performing Test CXX_FLAG__Wall
-- Performing Test CXX_FLAG__Wall - Success
-- Performing Test CXX_FLAG__Wextra
-- Performing Test CXX_FLAG__Wextra - Success
-- Performing Test CXX_FLAG__Winit_self
-- Performing Test CXX_FLAG__Winit_self - Success
-- Performing Test CXX_FLAG__Woverloaded_virtual
-- Performing Test CXX_FLAG__Woverloaded_virtual - Success
-- Performing Test CXX_FLAG__Wcast_qual
-- Performing Test CXX_FLAG__Wcast_qual - Success
-- Performing Test CXX_FLAG__Wpointer_arith
-- Performing Test CXX_FLAG__Wpointer_arith - Success
-- Performing Test CXX_FLAG__Wunused_local_typedef
-- Performing Test CXX_FLAG__Wunused_local_typedef - Failed
-- Performing Test CXX_FLAG__Wvla
-- Performing Test CXX_FLAG__Wvla - Success
-- Performing Test CXX_FLAG__Wgnu
-- Performing Test CXX_FLAG__Wgnu - Failed
-- Performing Test CXX_FLAG__Wno_gnu_zero_variadic_macro_arguments
-- Performing Test CXX_FLAG__Wno_gnu_zero_variadic_macro_arguments - Success
-- Performing Test CXX_FLAG__Wno_unused_function
-- Performing Test CXX_FLAG__Wno_unused_function - Success
-- Performing Test CXX_FLAG__Wno_noexcept_type
-- Performing Test CXX_FLAG__Wno_noexcept_type - Success
-- Enabling Thrust configuration: cpp.cpp.cpp14
-- Enabling Thrust configuration: cpp.cpp.cpp17
-- 2 unique thrust.host.device.dialect configurations generated
-- CPP system found?  TRUE
-- CUDA system found? FALSE
-- TBB system found?  TRUE
-- OMP system found?  TRUE
-- Configuring done
-- Generating done
-- Build files have been written to: /tmp/autopkgtest.tj8Hfd/autopkgtest_tmp
+ cd /tmp/autopkgtest.tj8Hfd/autopkgtest_tmp
+ make
Scanning dependencies of target thrust.cpp.cpp.cpp14.headers
[  0%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/addressof.h.cpp.o
[  0%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/adjacent_difference.h.cpp.o
[  0%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/advance.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/allocate_unique.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/binary_search.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/complex.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/copy.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/count.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_allocator.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_delete.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_free.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_make_unique.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_malloc.h.cpp.o
[  1%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_malloc_allocator.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_new.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_new_allocator.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_ptr.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_reference.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/device_vector.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/distance.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/equal.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/execution_policy.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/extrema.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/fill.h.cpp.o
[  2%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/find.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/for_each.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/functional.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/gather.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/generate.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/host_vector.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/inner_product.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/constant_iterator.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/counting_iterator.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/discard_iterator.h.cpp.o
[  3%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/iterator_adaptor.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/iterator_categories.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/iterator_facade.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/iterator_traits.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/permutation_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/retag.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/reverse_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/transform_input_output_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/transform_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/transform_output_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/iterator/zip_iterator.h.cpp.o
[  4%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/limits.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/logical.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/memory.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/merge.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mismatch.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/allocator.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/device_memory_resource.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/disjoint_pool.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/disjoint_sync_pool.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/disjoint_tls_pool.h.cpp.o
[  5%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/fancy_pointer_resource.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/host_memory_resource.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/memory_resource.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/new.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/polymorphic_adaptor.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/pool.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/pool_options.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/sync_pool.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/tls_pool.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/universal_memory_resource.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/mr/validator.h.cpp.o
[  6%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/optional.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/pair.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/partition.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/per_device_resource.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/discard_block_engine.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/linear_congruential_engine.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/linear_feedback_shift_engine.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/normal_distribution.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/subtract_with_carry_engine.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/uniform_int_distribution.h.cpp.o
[  7%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/uniform_real_distribution.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/random/xor_combine_engine.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/reduce.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/remove.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/replace.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/reverse.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/scan.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/scatter.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/sequence.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/set_operations.h.cpp.o
[  8%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/shuffle.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/sort.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/swap.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/error_code.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/system_error.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system_error.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/tabulate.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/transform.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/transform_reduce.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/transform_scan.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/tuple.h.cpp.o
[  9%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/integer_sequence.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/is_contiguous_iterator.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/is_execution_policy.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/is_operator_less_or_greater_function_object.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/is_operator_plus_function_object.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/is_trivially_relocatable.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/logical_metafunctions.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/remove_cvref.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/type_traits/void_t.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/uninitialized_copy.h.cpp.o
[ 10%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/uninitialized_fill.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/unique.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/universal_allocator.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/universal_ptr.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/universal_vector.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/version.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/zip_function.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/cpp/execution_policy.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/cpp/memory.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/cpp/memory_resource.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/cpp/pointer.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp14.headers.dir/headers/thrust.cpp.cpp.cpp14/system/cpp/vector.h.cpp.o
[ 11%] Built target thrust.cpp.cpp.cpp14.headers
Scanning dependencies of target thrust.cpp.cpp.cpp17.headers
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/addressof.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/adjacent_difference.h.cpp.o
[ 11%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/advance.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/allocate_unique.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/binary_search.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/complex.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/copy.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/count.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_allocator.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_delete.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_free.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_make_unique.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_malloc.h.cpp.o
[ 12%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_malloc_allocator.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_new.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_new_allocator.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_ptr.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_reference.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/device_vector.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/distance.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/equal.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/execution_policy.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/extrema.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/fill.h.cpp.o
[ 13%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/find.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/for_each.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/functional.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/gather.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/generate.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/host_vector.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/inner_product.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/constant_iterator.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/counting_iterator.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/discard_iterator.h.cpp.o
[ 14%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/iterator_adaptor.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/iterator_categories.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/iterator_facade.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/iterator_traits.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/permutation_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/retag.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/reverse_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/transform_input_output_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/transform_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/transform_output_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/iterator/zip_iterator.h.cpp.o
[ 15%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/limits.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/logical.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/memory.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/merge.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mismatch.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/allocator.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/device_memory_resource.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/disjoint_pool.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/disjoint_sync_pool.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/disjoint_tls_pool.h.cpp.o
[ 16%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/fancy_pointer_resource.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/host_memory_resource.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/memory_resource.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/new.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/polymorphic_adaptor.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/pool.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/pool_options.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/sync_pool.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/tls_pool.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/universal_memory_resource.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/mr/validator.h.cpp.o
[ 17%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/optional.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/pair.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/partition.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/per_device_resource.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/discard_block_engine.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/linear_congruential_engine.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/linear_feedback_shift_engine.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/normal_distribution.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/subtract_with_carry_engine.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/uniform_int_distribution.h.cpp.o
[ 18%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/uniform_real_distribution.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/random/xor_combine_engine.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/reduce.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/remove.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/replace.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/reverse.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/scan.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/scatter.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/sequence.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/set_operations.h.cpp.o
[ 19%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/shuffle.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/sort.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/swap.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/error_code.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/system_error.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system_error.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/tabulate.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/transform.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/transform_reduce.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/transform_scan.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/tuple.h.cpp.o
[ 20%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/integer_sequence.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/is_contiguous_iterator.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/is_execution_policy.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/is_operator_less_or_greater_function_object.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/is_operator_plus_function_object.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/is_trivially_relocatable.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/logical_metafunctions.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/remove_cvref.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/type_traits/void_t.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/uninitialized_copy.h.cpp.o
[ 21%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/uninitialized_fill.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/unique.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/universal_allocator.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/universal_ptr.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/universal_vector.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/version.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/zip_function.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/cpp/execution_policy.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/cpp/memory.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/cpp/memory_resource.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/cpp/pointer.h.cpp.o
[ 22%] Building CXX object CMakeFiles/thrust.cpp.cpp.cpp17.headers.dir/headers/thrust.cpp.cpp.cpp17/system/cpp/vector.h.cpp.o
[ 22%] Built target thrust.cpp.cpp.cpp17.headers
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.framework
[ 22%] Building CXX object testing/unittest/CMakeFiles/thrust.cpp.cpp.cpp17.test.framework.dir/thrust.cpp.cpp.cpp17/testframework.cu.cpp.o
[ 22%] Linking CXX static library ../../lib/libthrust.cpp.cpp.cpp17.test.framework.a
[ 22%] Built target thrust.cpp.cpp.cpp17.test.framework
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.zip_iterator_sort_by_key
[ 22%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.zip_iterator_sort_by_key.dir/thrust.cpp.cpp.cpp17/zip_iterator_sort_by_key.cu.cpp.o
[ 23%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.zip_iterator_sort_by_key
[ 23%] Built target thrust.cpp.cpp.cpp17.test.zip_iterator_sort_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.zip_iterator_scan
[ 23%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.zip_iterator_scan.dir/thrust.cpp.cpp.cpp17/zip_iterator_scan.cu.cpp.o
[ 23%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.zip_iterator_scan
[ 23%] Built target thrust.cpp.cpp.cpp17.test.zip_iterator_scan
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.vector_insert
[ 23%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.vector_insert.dir/thrust.cpp.cpp.cpp17/vector_insert.cu.cpp.o
[ 23%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.vector_insert
[ 23%] Built target thrust.cpp.cpp.cpp17.test.vector_insert
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.vector_allocators
[ 23%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.vector_allocators.dir/thrust.cpp.cpp.cpp17/vector_allocators.cu.cpp.o
[ 23%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.vector_allocators
[ 23%] Built target thrust.cpp.cpp.cpp17.test.vector_allocators
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.vector
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.vector.dir/thrust.cpp.cpp.cpp17/vector.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.vector
[ 24%] Built target thrust.cpp.cpp.cpp17.test.vector
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.universal_memory
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.universal_memory.dir/thrust.cpp.cpp.cpp17/universal_memory.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.universal_memory
[ 24%] Built target thrust.cpp.cpp.cpp17.test.universal_memory
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.unittest_tester
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.unittest_tester.dir/thrust.cpp.cpp.cpp17/unittest_tester.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.unittest_tester
[ 24%] Built target thrust.cpp.cpp.cpp17.test.unittest_tester
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.unique_by_key
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.unique_by_key.dir/thrust.cpp.cpp.cpp17/unique_by_key.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.unique_by_key
[ 24%] Built target thrust.cpp.cpp.cpp17.test.unique_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.uninitialized_copy
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.uninitialized_copy.dir/thrust.cpp.cpp.cpp17/uninitialized_copy.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.uninitialized_copy
[ 24%] Built target thrust.cpp.cpp.cpp17.test.uninitialized_copy
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.tuple_transform
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.tuple_transform.dir/thrust.cpp.cpp.cpp17/tuple_transform.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.tuple_transform
[ 24%] Built target thrust.cpp.cpp.cpp17.test.tuple_transform
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.tuple
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.tuple.dir/thrust.cpp.cpp.cpp17/tuple.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.tuple
[ 24%] Built target thrust.cpp.cpp.cpp17.test.tuple
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.trivial_sequence
[ 24%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.trivial_sequence.dir/thrust.cpp.cpp.cpp17/trivial_sequence.cu.cpp.o
[ 24%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.trivial_sequence
[ 24%] Built target thrust.cpp.cpp.cpp17.test.trivial_sequence
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.transform_scan
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.transform_scan.dir/thrust.cpp.cpp.cpp17/transform_scan.cu.cpp.o
[ 25%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.transform_scan
[ 25%] Built target thrust.cpp.cpp.cpp17.test.transform_scan
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.transform_iterator
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.transform_iterator.dir/thrust.cpp.cpp.cpp17/transform_iterator.cu.cpp.o
[ 25%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.transform_iterator
[ 25%] Built target thrust.cpp.cpp.cpp17.test.transform_iterator
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.transform_input_output_iterator
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.transform_input_output_iterator.dir/thrust.cpp.cpp.cpp17/transform_input_output_iterator.cu.cpp.o
[ 25%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.transform_input_output_iterator
[ 25%] Built target thrust.cpp.cpp.cpp17.test.transform_input_output_iterator
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.stable_sort_by_key_large
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.stable_sort_by_key_large.dir/thrust.cpp.cpp.cpp17/stable_sort_by_key_large.cu.cpp.o
[ 25%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.stable_sort_by_key_large
[ 25%] Built target thrust.cpp.cpp.cpp17.test.stable_sort_by_key_large
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.stable_sort_by_key
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.stable_sort_by_key.dir/thrust.cpp.cpp.cpp17/stable_sort_by_key.cu.cpp.o
[ 25%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.stable_sort_by_key
[ 25%] Built target thrust.cpp.cpp.cpp17.test.stable_sort_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.stable_sort
[ 25%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.stable_sort.dir/thrust.cpp.cpp.cpp17/stable_sort.cu.cpp.o
[ 26%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.stable_sort
[ 26%] Built target thrust.cpp.cpp.cpp17.test.stable_sort
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.tabulate
[ 26%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.tabulate.dir/thrust.cpp.cpp.cpp17/tabulate.cu.cpp.o
[ 26%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.tabulate
[ 26%] Built target thrust.cpp.cpp.cpp17.test.tabulate
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.sort
[ 26%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.sort.dir/thrust.cpp.cpp.cpp17/sort.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.sort
[ 27%] Built target thrust.cpp.cpp.cpp17.test.sort
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_union_key_value
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_union_key_value.dir/thrust.cpp.cpp.cpp17/set_union_key_value.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_union_key_value
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_union_key_value
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_union_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_union_descending.dir/thrust.cpp.cpp.cpp17/set_union_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_union_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_union_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_union_by_key_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_union_by_key_descending.dir/thrust.cpp.cpp.cpp17/set_union_by_key_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_union_by_key_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_union_by_key_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_descending.dir/thrust.cpp.cpp.cpp17/set_symmetric_difference_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key_descending.dir/thrust.cpp.cpp.cpp17/set_symmetric_difference_by_key_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key.dir/thrust.cpp.cpp.cpp17/set_symmetric_difference_by_key.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_symmetric_difference_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_intersection_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_intersection_descending.dir/thrust.cpp.cpp.cpp17/set_intersection_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_intersection_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_intersection_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_intersection_by_key_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_intersection_by_key_descending.dir/thrust.cpp.cpp.cpp17/set_intersection_by_key_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_intersection_by_key_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_intersection_by_key_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_intersection_by_key
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_intersection_by_key.dir/thrust.cpp.cpp.cpp17/set_intersection_by_key.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_intersection_by_key
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_intersection_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_difference_by_key_descending
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_difference_by_key_descending.dir/thrust.cpp.cpp.cpp17/set_difference_by_key_descending.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_difference_by_key_descending
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_difference_by_key_descending
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_difference_by_key
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_difference_by_key.dir/thrust.cpp.cpp.cpp17/set_difference_by_key.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_difference_by_key
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_difference_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_difference
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_difference.dir/thrust.cpp.cpp.cpp17/set_difference.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_difference
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_difference
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.scatter
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.scatter.dir/thrust.cpp.cpp.cpp17/scatter.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.scatter
[ 27%] Built target thrust.cpp.cpp.cpp17.test.scatter
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.scan_by_key
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.scan_by_key.dir/thrust.cpp.cpp.cpp17/scan_by_key.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.scan_by_key
[ 27%] Built target thrust.cpp.cpp.cpp17.test.scan_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.scan
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.scan.dir/thrust.cpp.cpp.cpp17/scan.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.scan
[ 27%] Built target thrust.cpp.cpp.cpp17.test.scan
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.set_intersection
[ 27%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.set_intersection.dir/thrust.cpp.cpp.cpp17/set_intersection.cu.cpp.o
[ 27%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.set_intersection
[ 27%] Built target thrust.cpp.cpp.cpp17.test.set_intersection
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.reverse
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.reverse.dir/thrust.cpp.cpp.cpp17/reverse.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.reverse
[ 28%] Built target thrust.cpp.cpp.cpp17.test.reverse
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.reduce_by_key
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.reduce_by_key.dir/thrust.cpp.cpp.cpp17/reduce_by_key.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.reduce_by_key
[ 28%] Built target thrust.cpp.cpp.cpp17.test.reduce_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.reduce
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.reduce.dir/thrust.cpp.cpp.cpp17/reduce.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.reduce
[ 28%] Built target thrust.cpp.cpp.cpp17.test.reduce
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.preprocessor
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.preprocessor.dir/thrust.cpp.cpp.cpp17/preprocessor.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.preprocessor
[ 28%] Built target thrust.cpp.cpp.cpp17.test.preprocessor
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.pair_sort_by_key
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.pair_sort_by_key.dir/thrust.cpp.cpp.cpp17/pair_sort_by_key.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.pair_sort_by_key
[ 28%] Built target thrust.cpp.cpp.cpp17.test.pair_sort_by_key
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.pair_sort
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.pair_sort.dir/thrust.cpp.cpp.cpp17/pair_sort.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.pair_sort
[ 28%] Built target thrust.cpp.cpp.cpp17.test.pair_sort
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.pair_scan
[ 28%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.pair_scan.dir/thrust.cpp.cpp.cpp17/pair_scan.cu.cpp.o
[ 28%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.pair_scan
[ 28%] Built target thrust.cpp.cpp.cpp17.test.pair_scan
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.pair_reduce
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.pair_reduce.dir/thrust.cpp.cpp.cpp17/pair_reduce.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.pair_reduce
[ 29%] Built target thrust.cpp.cpp.cpp17.test.pair_reduce
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.pair
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.pair.dir/thrust.cpp.cpp.cpp17/pair.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.pair
[ 29%] Built target thrust.cpp.cpp.cpp17.test.pair
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.out_of_memory_recovery
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.out_of_memory_recovery.dir/thrust.cpp.cpp.cpp17/out_of_memory_recovery.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.out_of_memory_recovery
[ 29%] Built target thrust.cpp.cpp.cpp17.test.out_of_memory_recovery
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.mr_pool
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.mr_pool.dir/thrust.cpp.cpp.cpp17/mr_pool.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.mr_pool
[ 29%] Built target thrust.cpp.cpp.cpp17.test.mr_pool
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.mismatch
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.mismatch.dir/thrust.cpp.cpp.cpp17/mismatch.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.mismatch
[ 29%] Built target thrust.cpp.cpp.cpp17.test.mismatch
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.metaprogamming
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.metaprogamming.dir/thrust.cpp.cpp.cpp17/metaprogamming.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.metaprogamming
[ 29%] Built target thrust.cpp.cpp.cpp17.test.metaprogamming
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.merge
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.merge.dir/thrust.cpp.cpp.cpp17/merge.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.merge
[ 29%] Built target thrust.cpp.cpp.cpp17.test.merge
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.max_element
[ 29%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.max_element.dir/thrust.cpp.cpp.cpp17/max_element.cu.cpp.o
[ 29%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.max_element
[ 29%] Built target thrust.cpp.cpp.cpp17.test.max_element
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.unique
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.unique.dir/thrust.cpp.cpp.cpp17/unique.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.unique
[ 30%] Built target thrust.cpp.cpp.cpp17.test.unique
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.logical
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.logical.dir/thrust.cpp.cpp.cpp17/logical.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.logical
[ 30%] Built target thrust.cpp.cpp.cpp17.test.logical
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.is_sorted_until
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.is_sorted_until.dir/thrust.cpp.cpp.cpp17/is_sorted_until.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.is_sorted_until
[ 30%] Built target thrust.cpp.cpp.cpp17.test.is_sorted_until
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.is_sorted
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.is_sorted.dir/thrust.cpp.cpp.cpp17/is_sorted.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.is_sorted
[ 30%] Built target thrust.cpp.cpp.cpp17.test.is_sorted
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.is_partitioned
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.is_partitioned.dir/thrust.cpp.cpp.cpp17/is_partitioned.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.is_partitioned
[ 30%] Built target thrust.cpp.cpp.cpp17.test.is_partitioned
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.inner_product
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.inner_product.dir/thrust.cpp.cpp.cpp17/inner_product.cu.cpp.o
[ 30%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.inner_product
[ 30%] Built target thrust.cpp.cpp.cpp17.test.inner_product
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.gather
[ 30%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.gather.dir/thrust.cpp.cpp.cpp17/gather.cu.cpp.o
[ 31%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.gather
[ 31%] Built target thrust.cpp.cpp.cpp17.test.gather
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.functional_placeholders_relational
[ 31%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.functional_placeholders_relational.dir/thrust.cpp.cpp.cpp17/functional_placeholders_relational.cu.cpp.o
[ 31%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.functional_placeholders_relational
[ 31%] Built target thrust.cpp.cpp.cpp17.test.functional_placeholders_relational
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.functional_bitwise
[ 31%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.functional_bitwise.dir/thrust.cpp.cpp.cpp17/functional_bitwise.cu.cpp.o
[ 31%] Linking CXX executable ../bin/thrust.cpp.cpp.cpp17.test.functional_bitwise
[ 31%] Built target thrust.cpp.cpp.cpp17.test.functional_bitwise
Scanning dependencies of target thrust.cpp.cpp.cpp17.test.for_each
[ 31%] Building CXX object testing/CMakeFiles/thrust.cpp.cpp.cpp17.test.for_each.dir/thrust.cpp.cpp.cpp17/for_each.cu.cpp.o
autopkgtest: DBG: timed out on ['/tmp/autopkgtest-qemu.cg9u5glm/runcmd'] ['su', '-s', '/bin/bash', 'openkylin', '-c', 'set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.tj8Hfd/build.8xK/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; exec /tmp/autopkgtest.tj8Hfd/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.tj8Hfd/command2-stderr --stdout=/tmp/autopkgtest.tj8Hfd/command2-stdout -- bash -ec \'debian/tests/upstream-testsuite CPP\' ;'] (kind: test)
autopkgtest [21:29:14]: ERROR: timed out on command "su -s /bin/bash openkylin -c set -e; export USER=`id -nu`; . /etc/profile >/dev/null 2>&1 || true;  . ~/.profile >/dev/null 2>&1 || true; buildtree="/tmp/autopkgtest.tj8Hfd/build.8xK/src"; mkdir -p -m 1777 -- "/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export AUTOPKGTEST_ARTIFACTS="/tmp/autopkgtest.tj8Hfd/command2-artifacts"; export ADT_ARTIFACTS="$AUTOPKGTEST_ARTIFACTS"; mkdir -p -m 755 "/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export AUTOPKGTEST_TMP="/tmp/autopkgtest.tj8Hfd/autopkgtest_tmp"; export ADTTMP="$AUTOPKGTEST_TMP"; export DEBIAN_FRONTEND=noninteractive; export LANG=C.UTF-8; export DEB_BUILD_OPTIONS=parallel=8; unset LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE   LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS   LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION LC_ALL;cd "$buildtree"; exec /tmp/autopkgtest.tj8Hfd/wrapper.sh --script-pid-file=/tmp/autopkgtest_script_pid --stderr=/tmp/autopkgtest.tj8Hfd/command2-stderr --stdout=/tmp/autopkgtest.tj8Hfd/command2-stdout -- bash -ec 'debian/tests/upstream-testsuite CPP' ;" (kind: test)
autopkgtest [21:29:14]: test command2: -----------------------]
autopkgtest: DBG: testbed executing test finished with exit status 1
autopkgtest: DBG: sending command to testbed: copyup /tmp/autopkgtest.tj8Hfd/command2-stdout /home/minami/Documents/openkylin-riscv/test/libthrust/command2-stdout
autopkgtest-virt-qemu: DBG: executing copyup /tmp/autopkgtest.tj8Hfd/command2-stdout /home/minami/Documents/openkylin-riscv/test/libthrust/command2-stdout
autopkgtest-virt-qemu: DBG: ['cmdls', "(['/tmp/autopkgtest-qemu.cg9u5glm/runcmd', 'sh', '-ec', 'cat </tmp/autopkgtest.tj8Hfd/command2-stdout'], ['cat'])"]
autopkgtest-virt-qemu: DBG: ['srcstdin', "<_io.BufferedReader name='/dev/null'>", 'deststdout', "<_io.BufferedWriter name='/home/minami/Documents/openkylin-riscv/test/libthrust/command2-stdout'>", 'devnull_read', <_io.BufferedReader name='/dev/null'>]
autopkgtest-virt-qemu: DBG:  +< /tmp/autopkgtest-qemu.cg9u5glm/runcmd sh -ec cat </tmp/autopkgtest.tj8Hfd/command2-stdout
autopkgtest-virt-qemu: DBG:  +> cat
autopkgtest-virt-qemu: DBG:  +>?
autopkgtest: DBG: got reply from testbed: timeout
autopkgtest: DBG: sending command to testbed: auxverb_debug_fail
autopkgtest-virt-qemu: DBG: executing auxverb_debug_fail
autopkgtest: DBG: got reply from testbed: ok
autopkgtest: DBG: TestbedFailure sent `auxverb_debug_fail', got `timeout', expected `ok...'
autopkgtest: DBG: testbed stop
autopkgtest: DBG: testbed close, scratch=/tmp/autopkgtest.tj8Hfd
autopkgtest: DBG: sending command to testbed: close
autopkgtest-virt-qemu: DBG: executing close
autopkgtest-virt-qemu: DBG: cleanup...
qemu-system-riscv64: terminating on signal 15 from pid 1112906 (/usr/bin/python3)
autopkgtest: DBG: got reply from testbed: ok
autopkgtest: DBG: sending command to testbed: quit
autopkgtest-virt-qemu: DBG: executing quit
autopkgtest-virt-qemu: DBG: cleanup...
autopkgtest: WARNING: Copying up test output timed out, ignoring
autopkgtest [21:34:15]: test command2:  - - - - - - - - - - results - - - - - - - - - -
command2             FLAKY timed out
autopkgtest: DBG: Skipping remaining log processing and testbed restore after timeout
```
- 特殊情况
  - 如result.csv出现测试例数为零的，则较大可能为初始化和解压源码时出错，需具体问题具体分析。