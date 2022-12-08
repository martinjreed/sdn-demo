Various notes on installation and configuration
===============================================

[Onos API](http://127.0.0.1:8181/onos/v1/docs/)

[Onos Flow Rules REST API JSON](https://wiki.onosproject.org/display/ONOS/Flow+Rules)

Output from STP example
-----------------------
```
*** Creating network
*** Adding hosts:
h1 h2 h3 h4 h5 
*** Adding switches:
s1 s2 s3 s4 
*** Adding links:
(20.00Mbit) (20.00Mbit) (s1, h1) (20.00Mbit) (20.00Mbit) (s1, h5) (10.00Mbit) (10.00Mbit) (s1, s2) (20.00Mbit) (20.00Mbit) (s2, h2) (10.00Mbit) (10.00Mbit) (s2, s3) (20.00Mbit) (20.00Mbit) (s3, h3) (10.00Mbit) (10.00Mbit) (s3, s4) (20.00Mbit) (20.00Mbit) (s4, h4) (10.00Mbit) (10.00Mbit) (s4, s1) 
*** Configuring hosts
h1 h2 h3 h4 h5 
*** Starting controller

*** Starting 4 switches
s1 s2 s3 s4 ...(20.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) 
Waiting for startup and network to settle (please wait 5 seconds)
*** STP state of the switches
s1-eth1=Designated
s1-eth2=Designated
s1-eth3=Root
s1-eth4=Designated
s2-eth1=Designated
s2-eth2=Alternate
s2-eth3=Root
s3-eth1=Designated
s3-eth2=Designated
s3-eth3=Root
s4-eth1=Designated
s4-eth2=Designated
s4-eth3=Designated
*** done printing STP state

*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 
h2 -> h1 h3 h4 h5 
h3 -> h1 h2 h4 h5 
h4 -> h1 h2 h3 h5 
h5 -> h1 h2 h3 h4 
*** Results: 0% dropped (20/20 received)

*** test1 Testing Throughput between H1 and H2 (no background traffic)
Please wait for 30 seconds
*** Results Throughput=9.422392Mb/s

waiting 20s for the buffers to empty
*** test2 Testing Throughput between H1 and H2 with background traffic between H4 and H3
Please wait for 30 seconds
*** Results Throughput from H4=4.791997Mb/s
*** Results Throughput from H1=4.780941Mb/s

waiting 20s for the buffers to empty
*** test3 Testing Simultaneous Throughput H1 to H2 and H5 to H2
Please wait for 30 seconds
*** Results Throughput from H5=4.888507Mb/s
*** Results Throughput from H1=4.678231Mb/s

waiting 20s for the buffers to empty
*** test4 Ping h4 to h3 10 times (including arp at beginning)
*** h4 : ('ping -c 10 10.0.0.3\n',)
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=1.04 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.064 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.233 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.072 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.101 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.061 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.060 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.061 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9198ms
rtt min/avg/max/mdev = 0.060/0.181/1.036/0.289 ms

*** test5 Ping h4 to h3 10 times (no arp at beginning)
*** h4 : ('ping -c 10 10.0.0.3\n',)
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.025 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.064 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.045 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.058 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.091 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.045 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.057 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.043 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.048 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.055 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9220ms
rtt min/avg/max/mdev = 0.025/0.053/0.091/0.016 ms

enter "quit" to exit or issue mininet commands if you know them
you can run the tests using the commands "test1" or "test2" ....
*** Starting CLI:
mininet> *** Stopping 0 controllers

*** Stopping 9 links
.........
*** Stopping 4 switches
s1 s2 s3 s4 
*** Stopping 5 hosts
h1 h2 h3 h4 h5 
*** Done
```
Output from SDN example
-----------------------
```
*** Creating network
*** Adding hosts:
h1 h2 h3 h4 h5 
*** Adding switches:
s1 s2 s3 s4 
*** Adding links:
(20.00Mbit) (20.00Mbit) (s1, h1) (20.00Mbit) (20.00Mbit) (s1, h5) (10.00Mbit) (10.00Mbit) (s1, s2) (20.00Mbit) (20.00Mbit) (s2, h2) (10.00Mbit) (10.00Mbit) (s2, s3) (20.00Mbit) (20.00Mbit) (s3, h3) (10.00Mbit) (10.00Mbit) (s3, s4) (20.00Mbit) (20.00Mbit) (s4, h4) (10.00Mbit) (10.00Mbit) (s4, s1) 
*** Configuring hosts
h1 h2 h3 h4 h5 
*** Starting controller
c0 
*** Starting 4 switches
s1 s2 s3 s4 ...(20.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) (10.00Mbit) (20.00Mbit) (10.00Mbit) 
Waiting for startup and network to settle (please wait 5 seconds)
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 
h2 -> h1 h3 h4 h5 
h3 -> h1 h2 h4 h5 
h4 -> h1 h2 h3 h5 
h5 -> h1 h2 h3 h4 
*** Results: 0% dropped (20/20 received)

*** test1 Testing Throughput between H1 and H2 (no background traffic)
Please wait for 30 seconds
*** Results Throughput=9.485832Mb/s

waiting 20s for the buffers to empty
*** test2 Testing Throughput between H1 and H2 with background traffic between H4 and H3
Please wait for 30 seconds
*** Results Throughput from H4=9.55411Mb/s
*** Results Throughput from H1=9.552325Mb/s

waiting 20s for the buffers to empty
*** test3 Testing Simultaneous Throughput H1 to H2 and H5 to H2
Please wait for 30 seconds
*** Results Throughput from H5=4.741033Mb/s
*** Results Throughput from H1=4.741039Mb/s

waiting 20s for the buffers to empty
*** test4 Ping h4 to h3 10 times (including arp at beginning)
    waiting 10s for any old flow rules to flush out
*** h4 : ('ping -c 10 10.0.0.3\n',)
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=9.77 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.858 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.074 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.050 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.080 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.064 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.061 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.087 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.052 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9174ms
rtt min/avg/max/mdev = 0.050/1.115/9.765/2.892 ms

*** test5 Ping h4 to h3 10 times (no arp at beginning)
    waiting 10s for any old flow rules to flush out
*** h4 : ('ping -c 10 10.0.0.3\n',)
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.615 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.088 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.073 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.066 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.051 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.080 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.066 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.055 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.078 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.107 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9203ms
rtt min/avg/max/mdev = 0.051/0.127/0.615/0.163 ms

enter "quit" to exit or issue mininet commands if you know them
you can run the tests using the commands "test1" or "test2" ....
*** Starting CLI:
mininet> *** Stopping 1 controllers
c0 
*** Stopping 9 links
.........
*** Stopping 4 switches
s1 s2 s3 s4 
*** Stopping 5 hosts
h1 h2 h3 h4 h5 
*** Done
```

Example of setting point intents from path information
------------------------------------------------------
```
paths --disjoint of:0000000000000001 of:0000000000000002
of:0000000000000001/2-of:0000000000000002/2; cost=1.0
of:0000000000000001/3-of:0000000000000004/3==>of:0000000000000004/2-of:0000000000000003/3==>of:0000000000000003/2-of:0000000000000002/3; cost=3.0
hosts
add-point-intent -s 0A:00:00:00:00:01 -d 0A:00:00:00:00:02 of:0000000000000001/1 of:0000000000000001/3
add-point-intent -s 0A:00:00:00:00:01 -d 0A:00:00:00:00:02 of:0000000000000004/3 of:0000000000000004/2
add-point-intent -s 0A:00:00:00:00:01 -d 0A:00:00:00:00:02 of:0000000000000003/3 of:0000000000000003/2
add-point-intent -s 0A:00:00:00:00:01 -d 0A:00:00:00:00:02 of:0000000000000002/3 of:0000000000000002/1
paths --disjoint of:0000000000000002 of:0000000000000001
of:0000000000000002/2-of:0000000000000001/2; cost=1.0
of:0000000000000002/3-of:0000000000000003/2==>of:0000000000000003/3-of:0000000000000004/2==>of:0000000000000004/3-of:0000000000000001/3; cost=3.0
add-point-intent -s 0A:00:00:00:00:02 -d 0A:00:00:00:00:01 of:0000000000000002/1 of:0000000000000002/3
add-point-intent -s 0A:00:00:00:00:02 -d 0A:00:00:00:00:01 of:0000000000000003/2 of:0000000000000003/3
add-point-intent -s 0A:00:00:00:00:02 -d 0A:00:00:00:00:01 of:0000000000000004/2 of:0000000000000004/3
add-point-intent -s 0A:00:00:00:00:02 -d 0A:00:00:00:00:01 of:0000000000000001/3 of:0000000000000001/1
```

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
