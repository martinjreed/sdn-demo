Various notes on installation and configuration
===============================================

Useful ONOS information
-----------------------

Pica8 QoS config
-----
[Pica8 QOs configuration guide](https://docs.pica8.com/display/PicOS211sp/Configuring+QoS+scheduler)

Linux TC notes
--------------

Note document from Southampton shows how to use tc commands rather than ovs_vsctl:

[Link to Southampton pdf guide on onos with tc](https://www.southampton.ac.uk/~drn1e09/ofertie/openflow_qos_mininet.pdf)
[Link to TC HTB guide](http://luxik.cdi.cz/~devik/qos/htb/manual/userg.htm)


``` bash
# make main root qdisc it has handle 1:0
# default traffic goes to queue 1:12
# using htb
sudo tc qdisc add dev s4-eth2 root handle 1: htb default 12; 
# add a root class with max 10Mbit 
sudo tc class add dev s4-eth2 parent 1: classid 1:1 htb rate 10Mbit ceil 10Mbit
# now we have children of 1:
# default has max 1Mbit but can borrow up to max
sudo tc class add dev s4-eth2 parent 1:1 classid 1:12 htb rate 1Mbit ceil 10Mbit
# 1:2 has max 1 Mbit and cannot borrow (useful for testing)
sudo tc class add dev s4-eth2 parent 1:1 classid 1:2 htb rate 1Mbit ceil 1Mbit
# 1:3 has max 9 Mbit but can borrow up to 10Mbit max
# note ideally rates should add up to parent max, but here am ignoring 1:2 as we
# will not actually use that
sudo tc class add dev s4-eth2 parent 1:1 classid 1:3 htb rate 9Mbit ceil 10Mbit
# 
# add a filter to put certain traffic into the 1:3 class (to give it more bandwidth than
# the default in 1:2)
sudo tc filter add dev s4-eth2 parent 1: prio 1 protocol ip u32 match ip src 10.0.0.1/32 classid 1:3
# useful output of classes:
sdn@sdn:~$ sudo tc -s -g class show dev s4-eth2
+---(1:1) htb rate 10Mbit ceil 10Mbit burst 1600b cburst 1600b 
     |    Sent 362339614 bytes 242108 pkt (dropped 0, overlimits 146652 requeues 0) 
     |    backlog 0b 0p requeues 0
     |
     +---(1:2) htb prio rate 1Mbit ceil 1Mbit burst 1600b cburst 1600b 
     |         Sent 685464 bytes 456 pkt (dropped 0, overlimits 454 requeues 0) 
     |         backlog 0b 0p requeues 0
     | 
     +---(1:12) htb prio rate 1Mbit ceil 10Mbit burst 1600b cburst 1600b 
     |          Sent 316614916 bytes 211895 pkt (dropped 3089, overlimits 163301 requeues 0) 
     |          backlog 0b 0p requeues 0
     | 
     +---(1:3) htb prio rate 9Mbit ceil 10Mbit burst 1598b cburst 1600b 
               Sent 45039234 bytes 29757 pkt (dropped 400, overlimits 4808 requeues 0) 
               backlog 0b 0p requeues 0
```
