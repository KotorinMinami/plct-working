# Unmatched freeBSD 安装启动

## 声明

- 本文档基于本人对freeBSD wiki 中[安装文档](https://wiki.freebsd.org/riscv/HiFiveUnmatched)的字面理解编写，该文章于2022-5-16编写，内容尚需验证。

- 截至 20210807，-CURRENT 和 13-STABLE 已支持 HiFive Unmatched，包括 USB、Ethernet 和 NVMe。

- 请注意，不支持 SD 卡镜像烧写，因为这需要mmc-spi-slot的驱动程序，而该驱动程序本身需要对 FreeBSD 的 spibus 进行彻底修改，以实现通过 SPI 直接控制 SDC/MMC 所需的更多低级功能，而无需中间控制器。

## 快速开始

以下步骤描述了如何将 FreeBSD 安装到 Unmatched 上的 NVMe drive。需要提供主板附带的 SD 卡，否则请参阅#Booting。

- 从FreeBSD 的[下载页面](https://download.freebsd.org/releases/riscv/riscv64/ISO-IMAGES/14.0/)下载 memstick 或 mini-memstick 安装程序的镜像。

- 将安装程序复制到 USB drive（u盘之类的），例如：
```
dd if=FreeBSD-14.0-CURRENT-riscv-riscv64-mini-memstick.img of=/dev/da1 bs=1m status=progress
```
- 将 SD 卡和 USB drive插入 Unmatched。给开发板上电。预期行为是直接启动到安装程序。

- 按照安装步骤操作，将 NVMe drive定位为根文件系统（很可能会显示为nda0）。

- 重新启动，并可以移除 USB drive。无论移除与否，主板都应该启动到新安装的系统。

- 如果没有 NVMe drive并希望从 USB drive 启动，请从下载页面选择 GENERICSD 映像。尽管名称如此，但它包含可以直接复制到 USB drive 的安装程序。

## Booting

### 附带sd卡分析

HiFive Unmatched 可以从板载闪存或 SD 卡加载第一阶段启动。该板附带一张 SD 卡，预装了 U-Boot 和 Linux。现在我们将使用提供的 SD 卡来启动。

根据参考手册，提供的卡上有四个分区：

| 分区 | 格式 | 描述 |
| --- | --- | --- |
| 1 | raw | U-Boot SPL |
| 2 | raw | U-Boot Proper |
| 3 | fat16 | Linux kernel、.dtb、... |
| 4 | ext4 | rootfs |

出于我们的目的，我们只关心前两个分区。U-Boot 将搜索 NVMe、USB，然后搜索 SD 卡

### u-boot镜像

由官方给出：[u-boot-sifive-fu740](https://www.freshports.org/sysutils/u-boot-sifive-fu740/)

### SD卡启动
要从 SD 卡启动，请确保板上的 MSEL[3:0] DIP 开关配置为 1011：

```
  +----------> CHIPIDSEL
  | +--------> MSEL3
  | | +------> MSEL2
  | | | +----> MSEL1
  | | | | +--> MSEL0
  | | | | |
 +-+-+-+-+-+
 | |X| |X|X| ON(1)
 | | | | | |
 |X| |X| | | OFF(0)
 +-+-+-+-+-+
BOOT MODE SEL

```

要将 u-boot 烧写到 SD 卡 （在linux平台），需要安装gdisk，然后执行以下命令（假设da0作为目标设备）：

```
# sgdisk -g --clear -a 1 \
    --new=1:34:2081 --change-name=1:spl --typecode=1:5B193300-FC78-40CD-8002-E86C45580B47 \
    --new=2:2082:10273 --change-name=2:uboot --typecode=2:2E54B353-1271-4842-806F-E436D6AF6985 \
    /dev/da0

# dd if=u-boot-spl.bin of=/dev/da0p1 bs=512 conv=sync
# dd if=u-boot.itb of=/dev/da0p2 bs=512 conv=sync
```
由于gdisk特性，需要所使用sgdisk保证u-boot分区的严格设置


### eMMC启动

要从内部闪存（SiFive 文档中的 QSPI0）启动，请将 MSEL[3:0] 设置为 0110：

```
  +----------> CHIPIDSEL
  | +--------> MSEL3
  | | +------> MSEL2
  | | | +----> MSEL1
  | | | | +--> MSEL0
  | | | | |
 +-+-+-+-+-+
 | | |X|X| | ON(1)
 | | | | | |
 |X|X| | |X| OFF(0)
 +-+-+-+-+-+
BOOT MODE SEL
```
要将 u-boot 烧写到 eMMC （linux下），请执行以下命令：

```
sgdisk -g --clear -a 1 \
  --new=1:40:2087         --change-name=1:spl --typecode=1:5B193300-FC78-40CD-8002-E86C45580B47 \
  --new=2:2088:10279      --change-name=2:uboot  --typecode=2:2E54B353-1271-4842-806F-E436D6AF6985 \
  --new=3:10280:10535     --change-name=3:env   --typecode=3:0FC63DAF-8483-4772-8E79-3D69D8477DE4 \
  /dev/mtdblock0

partprobe

dd if=u-boot-spl.bin of=/dev/mtdblock0 bs=4096 seek=5 conv=sync
dd if=u-boot.itb  of=/dev/mtdblock0 bs=4096 seek=261 conv=sync
```

经过以上烧写中的其中一个后，即可使用烧写的sd卡或eMMC启动安装程序。