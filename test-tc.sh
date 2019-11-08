#!/bin/bash


setTC() {
    IF=$1
    echo "Setting $IF"
    sudo tc qdisc del dev $IF root >/dev/null 2>&1
    sudo tc qdisc add dev $IF root handle 1: htb default 12;
    sudo tc class add dev $IF parent 1: classid 1:1 htb rate 10Mbit ceil 10Mbit
    sudo tc class add dev $IF parent 1:1 classid 1:6 htb rate 9Mbit ceil 10Mbit
    sudo tc class add dev $IF parent 1:1 classid 1:12 htb rate 1Mbit ceil 10Mbit
    sudo tc class add dev $IF parent 1:1 classid 1:3 htb rate 9Mbit ceil 10Mbit
}

interfaces="s1-eth2 s1-eth3 s2-eth2 s2-eth3 s3-eth2 s3-eth3"

for intf in $interfaces; do
    setTC $intf
done
