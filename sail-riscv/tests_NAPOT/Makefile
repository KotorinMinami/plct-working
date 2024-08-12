# 交叉编译器和工具链设置
CC_x86_64 = x86_64-linux-gnu-gcc
CC_arm = arm-linux-gnueabi-gcc
CC_riscv = riscv64-unknown-linux-gnu-gcc
Path_riscv = /home/minami/riscv-gnu-toolchain/bin

XLEN			:= 64
#TOOL_OPT		:= elf
TOOL_OPT		:= linux-gnu
#RISCV			:= /apps/vlsi/tools/riscv/gnu_toolchain/102020/standard/riscv64-unknown-elf
RISCV			:= /home/minami/riscv-gnu-toolchain
#RISCV			:= /opt/riscv${XLEN}
#CONFIG_BASE		:= 0x70080
MARCH          	:= -march=rv64imafdczkn_zicsr
#MARCH          	:= -march=rv32imc
#MARCH          	:= -march=elf32lriscv_ilp32
#RUN_TOOL		:= /home/billmc/riscv/sail-riscv.git/c_emulator/riscv_sim_RV32
GIT_ROOT_DIR	:= /home/minami/vscode/github/fork/sail-riscv
RUN_TOOL		:= ${GIT_ROOT_DIR}/c_emulator/riscv_sim_RV64


# 通用编译选项
MARCH := -march=rv64iczicsr
CFLAGS = -Wall -O2
LD_FILE := ./link.ld
LD_FLAGS = -static -T ${LD_FILE}
PWD := $(shell pwd)
ELF_DIR := elf
DUMP_DIR := dump
SRC_DIR := src
LOG_DIR := log

I_PATH = -I${PWD} -I${PWD}/env

ASM_SRC			:= $(wildcard ${SRC_DIR}/*.S ${SRC_DIR}*.s)
ASM_OBJS		:= $(patsubst ${SRC_DIR}/%.S,${ELF_DIR}/%.elf,${ASM_SRC}) 
ASM_FLAGS		:= ${MARCH} ${I_PATH} -DTEST_CASE_1=True -DXLEN=64 -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles -mabi=lp64 -T ${LD_FILE}
OBJDUMPFLAGS	= -t -Dz

RUN_FLAGS = --pmp-count=16

C_SRC		:= $(wildcard *.c)
C_OBJS		:= $(subst .c,.o,${C_SRC})
C_FLAGS		:= ${MARCH} ${I_PATH} 

OBJS		:= ${ASM_OBJS} ${C_OBJS}

BIN				:= ${RISCV}/bin

CC				:= ${BIN}/riscv${XLEN}-unknown-${TOOL_OPT}-gcc
ASM				:= ${BIN}/riscv${XLEN}-unknown-${TOOL_OPT}-gcc
LD				:= ${BIN}/riscv${XLEN}-unknown-${TOOL_OPT}-ld
#LD				:= ${BIN}/riscv${XLEN}-unknown-${TOOL_OPT}-gcc
OBJDUMP			:= ${BIN}/riscv${XLEN}-unknown-${TOOL_OPT}-objdump

TARGET			:= ${ASM_OBJS}
DUMP			:= $(patsubst ${ELF_DIR}/%.elf,${DUMP_DIR}/%.dump,${TARGET})
RUN_TARGET		:= $(patsubst ${ELF_DIR}/%.elf,${LOG_DIR}/%.log,${TARGET})

# 默认目标
all: build


${DUMP_DIR}/%.dump : ${ELF_DIR}/%.elf
	$(shell mkdir -p ${DUMP_DIR})
	${OBJDUMP} ${OBJDUMPFLAGS} $< > $@

${ELF_DIR}/%.elf	: $(SRC_DIR)/%.S
	$(shell mkdir -p $(ELF_DIR))
	${ASM}  ${ASM_FLAGS} -o $@ $<

${LOG_DIR}/%.log : ${ELF_DIR}/%.elf
	$(shell mkdir -p ${LOG_DIR})
	${RUN_TOOL} ${RUN_FLAGS} $< 2>&1 > $@

%.o	: %.c
	${CC} -c ${C_FLAGS} -o $@ $<

build: ${TARGET} ${DUMP}

# x86_64 目标
$(TARGET_x86_64): $(OBJ_x86_64)
	$(CC_x86_64) $(CFLAGS) -o $@ $^

# ARM 目标
$(TARGET_arm): $(OBJ_arm)
	$(CC_arm) $(CFLAGS) -o $@ $^

# 生成 x86_64 对象文件
%.x86_64.o: %.c
	$(CC_x86_64) $(CFLAGS) -c -o $@ $<

# 生成 ARM 对象文件
%.arm.o: %.c
	$(CC_arm) $(CFLAGS) -c -o $@ $<

# 清理
clean:
	rm -f $(OBJ_x86_64) $(OBJ_arm) $(TARGET_x86_64) $(TARGET_arm)


run: build ${RUN_TARGET}

.PHONY: all clean