# Debian系的自动化测试调研报告

## Debian的QA team职责
- 协调大量错误归档和变化
- 跟进没有行动的维护者([MIA](https://wiki.debian.org/qa.debian.org/MIATeam))
- 开发工具，例如[Debian Package Tracker](https://tracker.debian.org/)和 [Developer's Packages Overview](https://qa.debian.org/developer.php)
- 不断对整个档案进行系统检查，并将结果发布在 [piuparts.debian.org](https://piuparts.debian.org/) 和 [lintian.debian.org](https://lintian.debian.org/)。
这些结果也会显示在 PTS 中。(具有对应的软件包来进行测试）
- 关于各种问题（非常重要）的大量bug归档，这些问题或由piuparts/lintian检测到或通过重建整个存档检测到
- 对无人维护的包进行暂时的，及时的维护

## 自动化测试部分

### piuparts
- piuparts（package installation, upgrading and removal testing suite） 是一个用于测试 deb 包可以毫无问题地安装、升级和删除的工具。
- 今后移植可能用得到的[源码仓库](https://salsa.debian.org/debian/piuparts)
- 目前QA放到官方网页（https://piuparts.debian.org） 的一些[log](https://piuparts.debian.org/bullseye/)

![char.img](https://github.com/KotorinMinami/plct-working/blob/main/WorkReport/image/states_1.png)

                                                       样例通过与时间关系的图表
                                                       
### lintian
- Lintian 是一个全面的 Debian 软件包检查器。

它检测
- 是否违反Debian的协议和各种的子协议
- 是否是最佳的实现
- 是否有一些常见的错误
- 是否有以前维护者发现的问题

实现
- lintian的实现一般在安装包build后作为远程仓库的准入原则，或是QA对bug的查找

piuparts 与 lintian 均已被build为deb包，并在Debian的官方仓库中可供下载
