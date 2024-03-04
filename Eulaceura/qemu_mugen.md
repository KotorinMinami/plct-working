# Eulaceura 的 qemu 启动以及mugen配置

## 环境说明

- OS ： Archlinux

- qemu版本 ： 8.2.1

## 下载镜像

- [qemu镜像](https://mirror.iscas.ac.cn/openeuler-sig-riscv/eulaceura/image/23H2/Eulaceura.riscv64-23H2-Server_vm.qcow2)

- [bios固件](https://mirror.iscas.ac.cn/openeuler-sig-riscv/openEuler-RISC-V/testing/20231130/v0.1/QEMU/fw_payload_oe_uboot_2304.bin)使用oe-rv的bios

## 启动qemu

由于现在mugen内部逻辑问题，使用时为测试mugen是否能跑起来需要先配置一个tap 网卡

```shell
qemu-system-riscv64 \
  -nographic -machine virt \
  -smp 8 -m 8G \
  -bios fw_payload_oe_uboot_2304.bin \
  -drive file=Eulaceura.riscv64-23H2-Server_vm.qcow2,format=qcow2,id=hd0 \
  -object rng-random,filename=/dev/urandom,id=rng0 \
  -device virtio-rng-device,rng=rng0 \
  -device virtio-blk-device,drive=hd0 \
  -netdev tap,id=tapnet,ifname=tap0,downscript=no,script=no \
  -device virtio-net-pci,netdev=tapnet \
  -device virtio-net-device,netdev=usernet \
  -netdev user,id=usernet,hostfwd=tcp::12055-:22 \
  -device qemu-xhci -usb -device usb-kbd -device usb-tablet
```

## 配置mugen

- 安装

在Eulaceura中使用zypper进行update并下载git,如遇到core dump，可重置语言环境：
```shell
localectl set-locale zh _CN.UTF-8
zypper update
zypper install git
```

git clone上游mugen：

```shell
git clone https://gitee.com/openeuler/mugen.git
```

- 配置

    建议一步步验证完毕后备份快照在执行下一步

    - 配置mugen可执行：

    将[链接](https://github.com/KotorinMinami/mugen-riscv/tree/qemu/libs/locallibs)中的common_lib_python.sh ， get_test_device.py ， rpm_manage_eula.py复制到mugen/libs/locallibs/中（可使用scp），执行[dep_install_eula](https://github.com/KotorinMinami/mugen-riscv/blob/qemu/dep_install_eula.sh)安装依赖，此时给tap网卡配上一个ip并使用该ip配置mugen：
    ```shell
    bash mugen.sh -c --ip=$you_ip --user=root --password=Eulaceura12#$
    ```
    尝试运行测试htop看是否成功

    - 配置mugen_riscv.sh可执行

    将[链接](https://github.com/KotorinMinami/mugen-riscv/tree/qemu/libs/locallibs)中的mugen_riscv.py复制到mugen/libs/locallibs/中（可使用scp），将[mugen_riscv.sh](https://github.com/KotorinMinami/mugen-riscv/blob/qemu/mugen_riscv.sh)复制到mugen目录中，并使用如：
    ```shell
    echo htop > list_temp
    bash mugen_riscv.sh -l list_temp -x
    ```
    检验其是否正常运行，正常运行后退出虚拟机并保存镜像

    - 配置qemu_test.py可运行

    本地clone一个mugen并将[combination_parser.py](https://github.com/KotorinMinami/mugen-riscv/blob/qemu/combination_parser.py) , [qemu_test.py](https://github.com/KotorinMinami/mugen-riscv/blob/qemu/qemu_test.py) , [qemuVM.py](https://github.com/KotorinMinami/mugen-riscv/blob/qemu/qemuVM.py)复制到目录中，配置文件形如下：

    ```json
    {
        "workingDir":"/home/minami/Documents/Eulaceura/",
        "bios":"fw_payload_oe_uboot_2304.bin",
        "drive":"img_test.qcow2",
        "mugenDir":"/root/mugen",
        "threads":3,
        "cores":4,
        "memory":4,
        "mugenNative":1,
        "listFile":"oe2309test_1",
        "generate":1,
        "user":"root",
        "password":"Eulaceura12#$",
        "detailed":1,
        "addDisk":1,
        "bridge ip":"192.168.114.254",
        "tap num":50,
        "multiMachine":1,
        "addNic":1,
        "qemu option":"-machine virt "
    }
    ```
    试使用-F参数执行