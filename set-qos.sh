#!/bin/bash


setTC() {
    IF=$1
    sudo tc qdisc del dev $IF root >/dev/null 2>&1
    sudo tc qdisc add dev $IF root handle 1: htb default 3;
    sudo tc class add dev $IF parent 1: classid 1:1 htb rate 10Mbit ceil 10Mbit
    sudo tc class add dev $IF parent 1:1 classid 1:2 htb rate 9Mbit ceil 10Mbit
    sudo tc class add dev $IF parent 1:1 classid 1:3 htb rate 1Mbit ceil 10Mbit
}

for intf in $@; do
    setTC $intf
done
