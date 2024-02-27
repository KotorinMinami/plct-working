# 在Lichee Pi 4A上启动Eulaceura

## 镜像以及fastboot下载

- 烧录到sd卡上的[镜像](https://mirror.iscas.ac.cn/openeuler-sig-riscv/eulaceura/image/23H2/Eulaceura.riscv64-23H2-Desktop_Full.raw.xz)

- 烧录到eMMc中的[u-boot镜像](https://mirror.iscas.ac.cn/openeuler-sig-riscv/eulaceura/repos/plus/TH/firmware/bootfw-licheepi4A_1205.bin)

- 初始化eMMC的[RAM镜像](https://mirror.iscas.ac.cn/openeuler-sig-riscv/eulaceura/image/23H1/bootfw-lpi4aRAM.bin)

- fastboot下载：[fastboot](https://pan.baidu.com/e/1xH56ZlewB6UOMlke5BrKWQ)

## 烧录镜像

- 使用dd将包含boot分区与root分区的raw镜像烧录到sd卡中：
```shell
dd if=Eulaceura.riscv64-23H2-Desktop_Full.raw of=/dev/sda bs=1M status=progress
```

- 使用fastboot 烧录u-boot镜像：
```shell
sudo ./fastboot flash raw bootfw-lpi4aRAM.bin
sudo ./fastboot reboot
sleep  1
sudo ./fastboot flash uboot bootfw-licheepi4A_1205.bin
```

之后断开与电脑连接后插入sd卡并上电，即可进入系统