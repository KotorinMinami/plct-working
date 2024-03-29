# ACT现状

## RISC-V ISA 规范涉及内容过多，导致可配置的各种测试环境功能过于复杂

### 对于 Ratified Extension

-  Ratified Extensions即RISC-V ISA 中已经通过认定的扩展，在最新的riscv isa spec中未列出的部分，可以参阅[链接](https://wiki.riscv.org/display/HOME/Ratified+Extensions)

- ACT计划使用字符串旁匹配来过滤并配置对应的测试

### 对于WARL型寄存器的一些操作行为

#### 补充：WARL定义：

在RISC-V Zicsr扩展中讲到，RISC-V 定义了与每个 hart 相关的 4096 个控制和状态寄存器(csr)的单独地址空间。而CSR（Control and Status Register，控制与状态寄存器）具有以下主要用途：

- 配置和控制：CSR包含一系列寄存器，用于控制和配置处理器的各个方面，例如中断使能、时钟设置、异常处理等。
- 中断管理：CSR中的一些寄存器用于管理中断，包括中断开关、中断入口等信息。
- 存储器保护：CSR允许设置不同地址空间的存储器的访问属性，例如可读、可写、可执行等。
- 性能统计和调试接口：CSR中的某些字段用于性能统计，以及与调试器通信的接口。

这些CSR在不同特权级别下具有不同的访问权限，用于控制处理器的行为和状态。 

CSR寄存器中的字段存在各种类型，其中一种为 Write Any Values, Reads Legal Values (WARL) ， 其相关声明如：

某些读/写 CSR 字段允许写入任何值，同时保证每次读取时都返回合法值。假设编写 CSR 没有其他副作用，可以通过尝试写入所需的设置然后读取该值是否保留来确定支持的值的范围。这些字段在寄存器描述中标记为 WARL。

而由于在Zicsr中定义的CSR的读取顺序行为在某些情况下默认为弱顺序，同时WARL寄存器的读也具有很大的灵活度，具体确定这个行为指标就存在较大难度。

#### 叙述

- WARL字段行为可能的变化实际上是无限的

- ACT计划：目前已经实现了一个所有ACT和工具都将使用的工具(riscv-config)，它定义了通用合法值语法的模式，以及一组通用非法合法值的映射
    - 这是描述RISC-V 配置的规范方法，同时是运行ACT的必要条件
    - 强烈建议通过禁止写入来处理将非法值写入WARL字段的行为

### 对于不受CSR控制的情况（如：如何报告处理同时到来的同一优先级的异常）

- 在RISC-V ISA中，通常可以通过搜索“may”，“should”，“can”，“option”等词语来发现，报告并没有给出对应的详细清单。

- ACT计划：对此类未定义行为使用对应关键词以在riscv-config的YAML文件中声明，同时在sail中具体的实现这样的行为。

### 对于明确声明为依赖于实现的内容（WARL中的同样适用）

- ACT计划：避免测试这些行为

## 在SAIL中难以实现的特性

### 时序相关性（如：cycle ， realtime couters）

- 只有“no event”是架构相关的，只有InstRet计数器是可复现的（cycle 和 mtime不是）

- ACT计划：只测试架构相关以及可复现的行为，同时要求对应的实现来定义限制行为（如：mtime至少计数一次或者多次instret）

### 异步行为（如：interrupt ， concurrent access ， snoops ， DMA ， memory ops）

- ACT计划：实现与instret同步的伪事件生成器，通过不断模拟来确保不存在报错，同时实现一个新的或基于原有扩展的概率框架（而不是实际框架）以测试内存模型

### 非架构状态依赖以及不确定性行为

- 例子：如cache，TLBs(Translation Lookaside Buffer，缓存) , read/write/instruction buffers , predictors（指令预测）。

- ACT计划：向Sail中添加Cache与TLB支持，从而支持类似Spike的约束测试（高效的，同时使状态架构相关）

### 受约束的依赖于实现的选项不一定是固定的（如，未对齐情况下的加载）

- ACT计划：添加支持，允许trap/notrap两种情况的结果，否则认为选项是固定的，若非固定则舍弃这一行为（需要和Sail相结合）

## ACT计划工作总结

- 将Test_Format_Spec拆分并更新为
    
    - TestDev_Guideline_Spec:适用于测试开发人员

    - ACT_interface_Spec：适用于测试用户

- 关闭现有未解决Issue以及pr

- 添加对处理受限的非确定性结果（如未对齐的ld/st/br）和内存模型测试的支持

- 开发用于异步和并发测试的伪设备测试

   - 中断事件发生器

   - 内存事件生成器 （LR/SC,Atomic ops,WRS,mem model（TSO,WMO））

   - 调试跟踪命令接口（Etrace,Ntrace）

## ACT未来工作

- 与sail组合作
    - 添加使得CSR合法化以及TLB/Cache的支持
    - 开发SaiL as a Service 以及 Docker/Podman容器

- 工具开发
    - 更加简洁的覆盖语法（针对开发测试人员）
    - GUI riscv-config实现（针对测试用户）
    - riscv-config YAML配置匹配（使得可以使用特定的配置文件进行测试）
        - 具体而言为允许检查实现是否满足配置文件要求，即是由声称支持所需的扩展并通过每个扩展的测试

- 扩展 DUT Debug 支持
    - out-of-line GPR,FP以及Vector(CSR)的断言支持
    - 目前只有模型声明的GPR断言支持
    - 由于代码均为内联代码，此工作将花费大量精力
