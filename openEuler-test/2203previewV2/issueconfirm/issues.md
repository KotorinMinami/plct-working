# issue回归确认

## 已排除
### java-1.8.0-openjdk
- oe_test_openjdk_rmic_rmid
### easymock
- oe_test_easymock_junit4
- oe_test_easymock_junit5
### pcp
- oe_test_pmdumplog_02
- oe_test_pmevent_01
- oe_test_pmlogconf_pmlogsize
- oe_test_pmpython_mkaf_pcp-python
- oe_test_pmval_01

## 已修复


## 未修复

### java-1.8.0-openjdk
- oe_test_openjdk_appletviewer_clhsdb

failed_log
```
+ clhsdb
Error: Could not find or load main class sun.jvm.hotspot.CLHSDB
+ grep hsdb testlog
+ CHECK_RESULT 1
+ actual_result=1
+ expect_result=0
+ mode=0
+ error_log=
+ '[' -z 1 ']'
+ '[' 0 -eq 0 ']'
+ test 1x '!=' 0x
+ test -n ''
+ (( exec_result++ ))
+ LOG_ERROR 'oe_test_openjdk_appletviewer_clhsdb.sh line 42'
+ message='oe_test_openjdk_appletviewer_clhsdb.sh line 42'
+ python3 /root/mugen-riscv/libs/locallibs/mugen_log.py --level error --message 'oe_test_openjdk_appletviewer_clhsdb.sh line 42'
Fri Jan  6 12:46:34 2023 - ERROR - oe_test_openjdk_appletviewer_clhsdb.sh line 42
```
- oe_test_openjdk_jdb_jdep

failed_log
```
+ jfr help
+ grep 'jfr print'
oe_test_openjdk_jdb_jdeps.sh: line 55: jfr: command not found
+ CHECK_RESULT 1
+ actual_result=1
+ expect_result=0
+ mode=0
+ error_log=
+ '[' -z 1 ']'
+ '[' 0 -eq 0 ']'
+ test 1x '!=' 0x
+ test -n ''
+ (( exec_result++ ))
+ LOG_ERROR 'oe_test_openjdk_jdb_jdeps.sh line 56'
+ message='oe_test_openjdk_jdb_jdeps.sh line 56'
+ python3 /root/mugen-riscv/libs/locallibs/mugen_log.py --level error --message 'oe_test_openjdk_jdb_jdeps.sh line 56'
Fri Jan  6 13:24:26 2023 - ERROR - oe_test_openjdk_jdb_jdeps.sh line 56
+ return 0
+ jfr version
+ grep '[0-9]'
oe_test_openjdk_jdb_jdeps.sh: line 57: jfr: command not found
+ CHECK_RESULT 1
+ actual_result=1
+ expect_result=0
+ mode=0
+ error_log=
+ '[' -z 1 ']'
+ '[' 0 -eq 0 ']'
+ test 1x '!=' 0x
+ test -n ''
+ (( exec_result++ ))
+ LOG_ERROR 'oe_test_openjdk_jdb_jdeps.sh line 58'
+ message='oe_test_openjdk_jdb_jdeps.sh line 58'
+ python3 /root/mugen-riscv/libs/locallibs/mugen_log.py --level error --message 'oe_test_openjdk_jdb_jdeps.sh line 58'
Fri Jan  6 13:24:27 2023 - ERROR - oe_test_openjdk_jdb_jdeps.sh line 58
```
### easymock
- oe_test_easymock_spring

failed_log
```
+ javac -classpath '/usr/share/java/*:/usr/share/java/hamcrest/*:/usr/share/java/springframework/*:/usr/share/java/cglib/*:/usr/share/java/objenesis/*:' -d . OtherClass.java OurClass.java OurClassTest.java
OurClassTest.java:4: error: package org.springframework.test.util does not exist
import org.springframework.test.util.ReflectionTestUtils;
                                    ^
OurClassTest.java:18: error: cannot find symbol
        ReflectionTestUtils.setField(classUnderTest, "other", other);
        ^
  symbol:   variable ReflectionTestUtils
  location: class OurClassTest
OurClassTest.java:23: error: cannot find symbol
        ReflectionTestUtils.setField(classUnderTest, "other", other2);
        ^
  symbol:   variable ReflectionTestUtils
  location: class OurClassTest
3 errors
+ CHECK_RESULT 1
+ actual_result=1
+ expect_result=0
+ mode=0
+ error_log=
+ '[' -z 1 ']'
+ '[' 0 -eq 0 ']'
+ test 1x '!=' 0x
+ test -n ''
+ (( exec_result++ ))
+ LOG_ERROR 'oe_test_easymock_spring.sh line 30'
+ message='oe_test_easymock_spring.sh line 30'
+ python3 /root/GitRepo/mugen-riscv/libs/locallibs/mugen_log.py --level error --message 'oe_test_easymock_spring.sh line 30'
Fri Jan  6 03:28:35 2023 - ERROR - oe_test_easymock_spring.sh line 30
+ return 0
+ grep 'OK (1 test)'
+ java -classpath '/usr/share/java/*:/usr/share/java/hamcrest/*:/usr/share/java/springframework/*:/usr/share/java/cglib/*:/usr/share/java/objenesis/*:' org.junit.runner.JUnitCore OurClassTest
+ CHECK_RESULT 1
+ actual_result=1
+ expect_result=0
+ mode=0
+ error_log=
+ '[' -z 1 ']'
+ '[' 0 -eq 0 ']'
+ test 1x '!=' 0x
+ test -n ''
+ (( exec_result++ ))
+ LOG_ERROR 'oe_test_easymock_spring.sh line 32'
+ message='oe_test_easymock_spring.sh line 32'
+ python3 /root/GitRepo/mugen-riscv/libs/locallibs/mugen_log.py --level error --message 'oe_test_easymock_spring.sh line 32'
Fri Jan  6 03:28:39 2023 - ERROR - oe_test_easymock_spring.sh line 32
```
