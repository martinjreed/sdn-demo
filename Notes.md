Various notes on installation and configuration
===============================================

[Onos API](http://127.0.0.1:8181/onos/v1/docs/)

[Onos Flow Rules REST API JSON](https://wiki.onosproject.org/display/ONOS/Flow+Rules)


Useful ONOS information
-----------------------

``` bash
cloc
--------------------------------------------------------------------------------
Language                      files          blank        comment           code
--------------------------------------------------------------------------------
Java                           9103         166144         376389         766554
JSON                            852            190              0         188466
JavaScript                      265           9965          11363          45458
TypeScript                      248           2765           6056          17325
XML                             244           1647           3700          14597
CSS                             174           1800           3192           9762
Python                           91           2102           1604           9049
HTML                            169            505           1397           5477
Bourne Again Shell              188           1428           1198           5095
Markdown                         95           1551              0           4624
Bourne Shell                     37            495            390           1981
Maven                            22            177            384           1473
YAML                             25            108             80            934
Protocol Buffers                 55            196            985            734
Dockerfile                        1             13             21             48
make                              3             13              0             39
C Shell                           1              4             10             27
zsh                               1              2              4              5
--------------------------------------------------------------------------------
SUM:                          11574         189105         406773        1071648
--------------------------------------------------------------------------------
```


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
