#!/usr/bin/bash

function usage()
{
  echo "Usage: to set up tap : $1 br_ip tap_num br_name user"
  echo "                       for mugen-riscv qemu_test ,tap_num is more than 15"
  echo "                       br_name is the network bridge name ,default is br0. "
  echo "                       if you have no idea with it, just type 'sudo brctl show' "
  echo "                       to check out the name 'br0' haven't been used "
  echo "       to delete tap : $1 -d br_name"
  echo "                       it will delete all tap linked with the bridge br_name"
  echo "                       the bridge will be also deleted"
  echo "                       the default br_name will be 'br0'"
}

function create()
{
    modprobe tun
    brctl addbr $3
    ip address add $1"/24" dev $3
    for ((i = 0 ; i < $2 ; i++));
    do 
        tunctl -t "tap"$i -u $4
        brctl addif $3 "tap"$i
    done
    ip link set dev $3 up
    for ((i = 0 ; i < $2 ; i++));
    do 
        ip link set dev tap$i up
    done
}

function delete()
{
    taplist=($(brctl show | grep tap | awk '{print$1}'))
    flag=0
    for tap in ${taplist[@]};
    do
        if [ $tap == $1 ]; then
            flag=1
            now_tap=$(brctl show | grep $tap | awk '{print$4}')
        elif [ $flag -eq 1 ]; then
            now_tap=$tap
        else
            now_tap='null'
        fi
        if [ $now_tap != 'null' ]; then
            a=$(brctl delif $1 $now_tap)
            if [ $? -eq 0 ]; then
                tunctl -d $now_tap
            else 
                break
            fi
        fi
    done
    ip link set $1 down
    brctl delbr $1
}

if [[ $# -eq 4 ]]; then
  create $1 $2 $3 $4
elif [[ $# -eq 3 ]]; then
    create $1 $2 "br0" $3
elif [[ $(whoami) != "root" ]]; then
  echo "Error: must be root"
elif [ $# -eq 2 ] && [ $1 == "-d" ]; then
  delete $2
elif [ $# -eq 1 ] && [ $1 == "-d" ]; then
  delete "br0"
else
  usage $0
fi