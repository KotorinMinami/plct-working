#include "model_test.h"
#include "arch_test.h"
RVTEST_ISA("RV64I_Zicsr")

.section .text.init
.globl rvtest_entry_point
rvtest_entry_point:
RVMODEL_BOOT
RVTEST_CODE_BEGIN

//li x1, -1
//csrw pmpaddr0, x1 
//li x1, 0x0F
//csrw pmpcfg0, x1 
//li x1, -1
//srli x1, x1, 2
//csrw pmpaddr0, x1 
//li x1, 0x1F
//csrw pmpcfg0, x1  
li x3, 0x1000
csrw mscratch, x3
RVTEST_GOTO_LOWER_MODE Smode                

Smode_code:
li x1,0x1000
ld x2,(x1)
ld x2,0x500(x1)


RVTEST_CODE_END
RVMODEL_HALT

RVTEST_DATA_BEGIN
.align 4

rvtest_data:
.word 0xbabecafe
.word 0xbabecafe
.word 0xbabecafe
.word 0xbabecafe
RVTEST_DATA_END


RVMODEL_DATA_BEGIN
rvtest_sig_begin:
sig_begin_canary:
CANARY;


signature_x1_0:
    .fill 0*(XLEN/32),4,0xdeadbeef


signature_x1_1:
    .fill 1*(XLEN/32),4,0xdeadbeef

#ifdef rvtest_mtrap_routine

tsig_begin_canary:
CANARY;
mtrap_sigptr:
    .fill 64*(XLEN/32),4,0xdeadbeef
tsig_end_canary:
CANARY;

#endif

#ifdef rvtest_gpr_save

gpr_save:
    .fill 32*(XLEN/32),4,0xdeadbeef

#endif

sig_end_canary:
CANARY;
rvtest_sig_end:
RVMODEL_DATA_END

