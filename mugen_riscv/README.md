# Mugen riscv并入上游要点
## 现状
> Todo：整理证据，报告
### 并入的重要性
### 目前相较于mugen上游的做出的成果
- 经过验证mugen的大部分脚本可以直接适用于openEuler-RISCV qemu的自动化测试:[res_list]()
- 经过开发编写以及实测验证，已经开发了针对RISCV与x86架构的qemu镜像可在PC设备上进行自动多线程测试的脚本:[介绍]()
- 针对目前所有mugen的脚本，已经有针对出现兼容性问题的脚本进行分析的结果，具体修改方案待商榷
### 兼容性以及RISCV目前的问题
- mugen上游的脚本仍有一些具有兼容性问题其中包括但不限于：
- - mugen脚本对于测试环境的准备标准各有差异
- - grep输出由于没有考察RISCV的环境对应输出造成缺陷误判
- - 目前openEuler-RISCV使用的仍是qemu镜像，其与mugen脚本的兼容性以及与实体机的性能差异造成测试的误判
- openEuler-RISCV自身存在问题
- - qemu的模拟对测试环境的复现程度的问题
### mugen上游仓库公开的脚本存在一定历史遗留问题
## 合入方案（我方提出+商讨+定案分工）
> Todo:思考合理方案，准备
### 对于目前的脚本成果
- 合入mugen仓库（或许需要将代码规范向mugen/lib中脚本规范靠拢）
- 已经修改过的脚本，判断是否尽量满足三种架构均进行适配的情况，考虑对此进行进一步适配
- 目前已经分析出问题的脚本，考虑做出修改，或与上游商讨修改方案
### 对于目前的问题合入时的商讨
- 上游对于ARM架构在qemu中的测试方案与RISCV mugen的测试方案的对比
- - 包括测试环境的要求，测试样例的范围限制，etc.
- 对于目前上游存在一定问题的仓库，上游的测试应对方案，以及脚本修改涉及的各类问题，商讨解决方案
- 合入方案的商讨
- - 若对仓库中脚本的修改仍的不出结论，应确定合理的测试方针，并再之后共同完善mugen公开出来的仓库
- - 得出结论的商讨合入方案：一次对之前出现问题的做出修改 or 调整测试策略并完善脚本
### 合入后的维护方案