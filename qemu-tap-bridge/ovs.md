# 使用ovs来配置网桥实现qemu多机互通的方法及与Linux Bridge的比较

## Open vSwitch
    
Open vSwitch（缩写 OVS）是一个高质量的，多层虚拟交换机(网络分层的层)，其目的是让大规模网络自动化可以通过编程扩展，同时仍然支持标准的管理接口和协议：NetFlow. SFlow ... 等，并且它还支持多个物理机的分布式环境。开放源代码的软件定义网络（SDN）实现，由Open Networking Foundation（缩写 ONF）开发。

## 为什么要使用ovs

相较于Linux Bridge集成在Linux内核代码中，比较简单，ovs使用systemd来守护进程，支持功能更多，且性能发挥更强，转发更加稳定，能够缓解mugen高负载运行下出现的断联等guest之间多机互通问题。

## 网桥配置

### 软件安装

- Archlinux：
```
# sudo pacman -S openvswitch
```

- Debian：
```
# sudo apt-get install openvswitch-switch openvswitch-common
```

### 配置网桥
>注：此处参照[Arch Wiki](https://wiki.archlinux.org/title/Open_vSwitch)配置比较多，且在Archlinux验证可用

- 启动systemd：
```
# sudo systemctl start ovs-vswitchd.service
``` 

- 创建网桥：
```
# sudo ovs-vsctl add-br br0
```

- 创建tap网卡：
可如[在qemu下使用网桥以及tap的方式使得多个虚拟机之间可以互通](./readme.md)中方案创建，也可使用ip指令配置：
```
# ip tuntap add dev tap0 mod tap
# ip link set dev tap0 up
```

- 添加bridge端口：
```
# ovs-vsctl add-port br0 tap0
```
之后操作如上文提及一般，设置多个tap网卡，配置虚拟机网卡为tap模式，guest中配置同一局域网中ip，实现互联，这里不再赘述

## ovs与Linux Bridge比较

### 性能

OVS使用硬件加速技术，如Open vSwitch kernel module和OpenFlow协议，因此具有更高的性能。而Linux Bridge主要依赖软件实现，集成在内核之中，无需ovs一般占用进程资源，占用较低。

### 安装和使用

OVS需要安装Open vSwitch软件包，并配置相应的网络接口，而Linux Bridge不需要额外的安装步骤，开箱即用

### 稳定性

实测中ovs在mugen的一些复杂的拓扑环境下能更好的保证互通的概率,可以减少mugen某些测试例的误判，而linux bridge则容易在某些情况下出现断联的情况，且在mugen高负载运行下，linux bridge容易产生一些异常情况。