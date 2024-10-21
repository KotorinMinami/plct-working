# 2.26-3.3 工作报告

- 在Lichee Pi 4A 上成功刷写并运行Eulaceura，观察到1205对应的固件无法使Lichee Pi 4A的风扇正常工作：[刷写启动](https://github.com/KotorinMinami/plct-working/blob/main/Eulaceura/lichee_pi_4a_boot.md)

- 针对Eulaceura使用的zypper的包管理，编写相关的mugen套件，以支持使用zypper进行包管理：[commit](https://github.com/KotorinMinami/mugen-riscv/commit/7110aa2993a59496a95a076c174e85231e32efa3)