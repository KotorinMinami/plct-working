# RAIL-RISCV 模型调研

## sail简介

Sail 是一种用于描述指令集架构的语言 （ISA） 处理器的语义。旨在提供工程师友好型、类似供应商伪代码的方式来描述指令语义。它本质上是一阶命令语言，但包含数值类型和位向量长度。Sail 被用于多个 ISA 描述，包括 Armv8-A 顺序行为的基本完整版本、RISC-V、MIPS、CHERI-RISC-V 和 CHERI-MIPS;所有这些ISA都是完备的足以启动各种操作系统。还有针对 IBM POWER 和 x86 较小片段的 Sail 模型。

## SAIL-RISCV简介

Sail-RiSCV是一个用Sail语言编写的RISC-V架构的形式化规范，基于此规范，我们可以编写与之相关的编译器，解释器，构建汇编文件，elf可执行文件，虚拟执行软件等

## SAIL-RISCV Model 编译构建

> 以下大多数均基于rail-riscv仓库教程编写，验证环境为Archlinux

### 环境准备

- 安装opam,以及对应编译依赖：

    ```
    sudo pacman -S opam zlib pkgconf gmp z3
    ```

    注： opam要求版本为4.08.1及以上，若软件仓库中版本过低，可使用`opam switch`进行更新

    ```
    opam switch create 5.1.0
    ```

- 配置ocaml运行环境：

    ```
    eval $(opam config env)
    ```

- 安装sail编译器

    ```
    opam install sail
    ```

    安装完成后可查看sail版本验证是否配置正常：
    
    ```
    which sail
    sail --help
    ```

### 编译

- 下载源码：

    ```
    git clone https://github.com/riscv/sail-riscv.git
    ```

- 编译：

    进入目录后，可以看到有对应脚本`build_simulators。sh`，执行并等待编译完成后便可看到对应文件夹中存在对应32位及64位的模拟器
    
    ```
    ./build_simulators.sh
    # 执行完成后
    ls -l c_emulator/ | grep RV
    -rwxr-xr-x 1 minami minami 14544048 Nov  3 08:08 riscv_sim_RV32
    -rwxr-xr-x 1 minami minami 14797616 Nov  3 08:11 riscv_sim_RV64
    ```

### 运行

- 运行elf文件
    
    对应test/riscv-tests中elf文件均可对应运行

    ```
    ./c_emulator/riscv_sim_RV64 ./test/riscv-tests/rv64um-v-div.elf
    ```

    其中ocaml的需要安装dtc

    ```
    sudo pacman -S dtc
    ```

- 运行Linux Boot Image

    ```
    dtc < os-boot/rv64-64mb.dts > os-boot/rv64-64mb.dtb

    ./c_emulator/riscv_sim_RV64 -b os-boot/rv64-64mb.dtb -t /tmp/console.log os-boot/rv64-linux-4.15.0-gcc-7.2.0-64mb.bbl > >(gzip -c > execution-trace.log.gz) 2>&1

    tail -f /tmp/console.log
    ```

    