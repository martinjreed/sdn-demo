#!/usr/bin/python

"""
Simple example of setting network and CPU parameters

NOTE: link params limit BW, add latency, and loss.
There is a high chance that pings WILL fail and that
iperf will hang indefinitely if the TCP handshake fails
to complete.
"""

import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from tempfile import mkstemp
from subprocess import check_output
import re
import time
import os

from sys import argv

class SquareTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        switch1 = self.addSwitch('s1', cls=OVSSwitch, failMode="standalone")
        switch2 = self.addSwitch('s2', cls=OVSSwitch, failMode="standalone")
        switch3 = self.addSwitch('s3', cls=OVSSwitch, failMode="standalone")
        switch4 = self.addSwitch('s4', cls=OVSSwitch, failMode="standalone")
        host1 = self.addHost("h1")
        host2 = self.addHost("h2")
        host3 = self.addHost("h3")
        host4 = self.addHost("h4")
        print(opts)
        #note in the code HTB seems to be the default but does not work well
        # spent some time trying out these. In practice it may depend upon the TC values
        # put in by mininet/mininet/link.py so this may vary from kernel to kernel
        # and different mininet releases
        # the best results seem to be with the following:
        use_tbf=True
        use_hfsc=False
        # have not tried this, probably not relevant unless the app makes use of ECN
        enable_ecn=False
        # while in theory it makes sense to enable this, the problem is that
        # it might delete some of the essential iperf packets so probably best left off
        enable_red=False
        self.addLink(switch1,host1,bw=20,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch2,host2,bw=20,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch3,host3,bw=20,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch4,host4,bw=20,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)

        self.addLink(switch1,switch2,bw=10,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch2,switch3,bw=10,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch3,switch4,bw=10,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        self.addLink(switch4,switch1,bw=10,use_tbf=use_tbf,
                     use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)

def throughputTestWithBackground(net):
    print("*** test2 Testing Throughput between H1 and H2 with background traffic between H4 and H3")
    print("Please wait for 30 seconds")
    h1 = net.getNodeByName("h1")
    h2 = net.getNodeByName("h2")
    h3 = net.getNodeByName("h3")
    h4 = net.getNodeByName("h4")
    # for udp
    #h2.cmd("iperf -s -u &")
    #h3.cmd("iperf -s -u &")
    h2.cmd("iperf -s &")
    h3.cmd("iperf -s &")
    time.sleep(4)
    # for udp
    #h4.cmd("iperf -c 10.0.0.3 -u -b 10M -t 35 &")
    h4.cmd("iperf -c 10.0.0.3 -t 35 &")
    time.sleep(2)
    # for udp
    #h1out = h1.cmd("iperf -c 10.0.0.2 -u -b 10M -t 30 -y c -x CDMS")
    h1out = h1.cmd("iperf -c 10.0.0.2 -t 30 -y c")
    h1out = h1out.split(",")
    if len(h1out) < 9:
        print("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)")
        print("***      note that these UDP tests might fail due to the fact the network is being overloaded")
        print("***      you can run it again later from the command line as test2.")
    else:
        tp=float(h1out[8])/1000000.0
        print("*** Results Throughput=" +str(tp) + "Mb/s")

def throughputTest(net):
    print("*** test1 Testing Throughput between H1 and H2 (no background traffic)")
    print("Please wait for 30 seconds")
    h1 = net.getNodeByName("h1")
    h2 = net.getNodeByName("h2")
    h3 = net.getNodeByName("h3")
    h4 = net.getNodeByName("h4")
    # for udp
    #h2.cmd("iperf -s -u &")
    h2.cmd("iperf -s &")
    time.sleep(4)
    # for udp
    #h1out = h1.cmd("iperf -c 10.0.0.2 -u -b 10M -t 30 -y c -x CDMS")
    h1out = h1.cmd("iperf -c 10.0.0.2 -t 30 -y c")
    h1out = h1out.split(",")
    if len(h1out) < 9:
        print("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)")
        print("***      note that these UDP tests might fail due to the fact the network is being overloaded")
        print("***      you can run it again later from the command line as test1.")
    else:
        tp=float(h1out[8])/1000000.0
        print("*** Results Throughput=" +str(tp) + "Mb/s")
    
def test1(self,line):
    net = self.mn
    throughputTest(net)

def test2(self,line):
    net = self.mn
    throughputTestWithBackground(net)
    
    
def printSTP():
    # get the list of ports, this is nasty
    ports=check_output('sudo ovs-vsctl list port | grep name | grep "-" | sed "s/.*name.*: \\"\(.*\)\\"$/\\1/" | sort',shell=True)
    # for each port
    for i in ports.splitlines():
        reply=check_output("/usr/bin/ovs-vsctl list port " + i,shell=True)
        reply=reply.replace("\n"," ")
        # again nasty
        filtered = re.sub(r'.*name[^"]+"([^"]+)".*rstp_port_role(.*),.*$',r'\1\2',reply)
        print(filtered)

    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--sdn", action='store_true', help="enable SDN mode (the default)")
    group.add_argument("-n", "--normal", action='store_true', help="enable STP mode (not the default)")
    args = parser.parse_args()
    if args.normal == False:
        args.sdn = True
    if args.sdn == True:
        print("Running in SDN mode")
    else:
        print("Running in STP mode")
    # kill any old mininet first
    os.system("mn -c > /dev/null 2>&1")    
    setLogLevel( 'info' )

    topo = SquareTopo( )
    net = Mininet( topo=topo,
                   link=TCLink,
                   controller=None)
    if args.sdn :
        net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

    net.start()
    s1=net.getNodeByName('s1')
    s2=net.getNodeByName('s2')
    s3=net.getNodeByName('s3')
    s4=net.getNodeByName('s4')
    if args.sdn == False :
        s4.cmd("ovs-vsctl set Bridge s4 rstp_enable=true ")
        s4.cmd("ovs-vsctl set Bridge s4 other_config:rstp-priority=4096")
        s3.cmd("ovs-vsctl set Bridge s3 rstp_enable=true")
        s4.cmd("ovs-vsctl set Bridge s3 other_config:rstp-priority=28672")
        s1.cmd("ovs-vsctl set Bridge s1 rstp_enable=true")
        s2.cmd("ovs-vsctl set Bridge s2 rstp_enable=true")
    
    print "*** Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "*** Dumping switch connections"
    dumpNodeConnections(net.switches)
    print("Waiting for startup and network to settle (please wait 30 seconds)")
    time.sleep(45)
    if args.sdn == False  :
        print("*** STP state of the switches")
        printSTP()
        print("*** done printing STP state")
    
    net.pingAll()
    throughputTest(net)
    throughputTestWithBackground(net)

    CLI.do_test1 = test1
    CLI.do_test2 = test2
    print("enter \"quit\" to exit or issue mininet commands if you know them")
    print("you can also repeat the two throughput tests using the commands \"test1\" or \"test2\"")
    CLI(net)
    net.stop()
