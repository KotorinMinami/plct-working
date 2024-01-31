# DynomaRIO 的编译使用

## DynomaRIO介绍

DynamoRIO是一个运行时代码操纵系统，支持在程序执行时对程序的任何部分进行代码转换。DynamoRIO导出用于构建动态工具的接口，用于多种用途：程序分析和理解、分析、检测、优化、翻译等。DynamoRIO可以在Android, Linux, 和 Windows操作系统下运行。

本文演示在RISC-V架构平台下，进行DynamoRIO的编译和运行。

## 编译

### 环境准备

- OS:Debian unstable RISC-V QEMU

- 安装依赖：
    ```bash
    apt-get install cmake g++ g++-multilib doxygen git zlib1g-dev libunwind-dev libsnappy-dev liblz4-dev
    ```

- 下载源码：
    ```bash
    git clone --recurse-submodules -j4 https://github.com/ksco/dynamorio.git
    ```

## 编译

- Cmake生成makefile：
    ```bash
    cd dynamorio && mkdir build && cd build
    cmake ..
    ```

- 编译：
    ```bash
    make -j4
    ```

- 编译成功后，会在build/bin64目录下生成dynamorio的可执行文件。

## 运行

- 运行DynamoRIO：DynamoRIO的运行需要指定一个DR运行时，DR运行时是一个DynamoRIO的插件，它负责执行DynamoRIO的插件。可使用`-t`参数指定。如：

    ```bash
    bin64/drrun -t drcov -- application arg1 arg2
    ```

    运行成功后，会在当前目录下生成一个`drcov.out`文件。记录对应的log

- 此处我们仅在riscv下验证其是否能够正常识别riscv架构的ELF，所以直接运行`bin64/drrun`即可。

- 样例程序：
    ```cpp
    #include <iostream>

    int main(){
      std::cout << "Hello, world!" << std::endl;
      return 0;
    }
    ```

- 编译后试运行：
    ```
    root@debian:~# g++ -o hello hello_test.cpp
    root@debian:~# ./hello 
    Hello world!
    ```

- 运行DynamoRIO：
    ```
    root@debian:~# dynamorio/build/bin64/drrun hello
    Hello world!
    ```
    可看到其正常运行