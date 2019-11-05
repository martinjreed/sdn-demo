#!/bin/bash

IF=s4-eth2

sudo tc qdisc add dev $IF root handle 1: htb default 12; 
sudo tc class add dev $IF parent 1:1 classid 1:12 htb rate 1Mbit ceil 10Mbit
sudo tc class add dev $IF parent 1:1 classid 1:3 htb rate 9Mbit ceil 10Mbit
