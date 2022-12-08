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
from mininet.log import setLogLevel, output, info
from mininet.cli import CLI
from tempfile import mkstemp
from subprocess import check_output, call
import re
import time
import os

from sys import argv


class SquareTopo(Topo):
    "Square switch topology with five hosts"
    def __init__(self, qos, **opts):
        Topo.__init__(self, **opts)
        switch1 = self.addSwitch('s1', cls=OVSSwitch, failMode="standalone", protocols="OpenFlow13")
        switch2 = self.addSwitch('s2', cls=OVSSwitch, failMode="standalone", protocols="OpenFlow13")
        switch3 = self.addSwitch('s3', cls=OVSSwitch, failMode="standalone", protocols="OpenFlow13")
        switch4 = self.addSwitch('s4', cls=OVSSwitch, failMode="standalone", protocols="OpenFlow13")
        host1 = self.addHost("h1", mac='0a:00:00:00:00:01')
        host2 = self.addHost("h2", mac='0a:00:00:00:00:02')
        host3 = self.addHost("h3", mac='0a:00:00:00:00:03')
        host4 = self.addHost("h4", mac='0a:00:00:00:00:04')
        host5 = self.addHost("h5", mac='0a:00:00:00:00:05')

        # this is the default
        if qos == False:
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
            # putting host5 last keeps the port numbers in a nice order
            # ie 1 for primary host, 2,3 for switch links, this
            # one is an odd one out in port 4
            self.addLink(switch1,host5,bw=20,use_tbf=use_tbf,
                         use_hfsc=use_hfsc,enable_ecn=enable_ecn,enable_red=enable_red)
        else:
            self.addLink(switch1,host1)
            self.addLink(switch2,host2)
            self.addLink(switch3,host3)
            self.addLink(switch4,host4)
            
            self.addLink(switch1,switch2)
            self.addLink(switch2,switch3)
            self.addLink(switch3,switch4)
            self.addLink(switch4,switch1)
            # putting host5 last keeps the port numbers in a nice order
            # ie 1 for primary host, 2,3 for switch links, this
            # one is an odd one out in port 4
            self.addLink(switch1,host5)
        
    def afterStartConfig(self, net, sdn, qos):
        """configuration to topo that needs doing after starting"""
        s1=net.getNodeByName('s1')
        s2=net.getNodeByName('s2')
        s3=net.getNodeByName('s3')
        s4=net.getNodeByName('s4')
        # this is fairly manual, we want to make s1-s2 link off in STP
        # so setting S4 to be root and s3 secondary root
        # also enabling rstp for quicker startup
        if sdn == False :
            s4.cmd("ovs-vsctl set Bridge s4 rstp_enable=true ")
            s4.cmd("ovs-vsctl set Bridge s4 other_config:rstp-priority=4096")
            s3.cmd("ovs-vsctl set Bridge s3 rstp_enable=true")
            s3.cmd("ovs-vsctl set Bridge s3 other_config:rstp-priority=28672")
            s1.cmd("ovs-vsctl set Bridge s1 rstp_enable=true")
            s2.cmd("ovs-vsctl set Bridge s2 rstp_enable=true")
        # not the default
        if qos == True:
            setTCcmd=os.path.dirname(os.path.realpath(__file__))+"/set-qos.sh"
            # get the list of interfaces that are between switches only (ie ignore lo and host interfaces)
            tcInterfaces = ''
            for sw in net.switches:
                for intf in sw.intfList():
                    if intf.link:
                        intfName = intf.name
                        # this is brittle, but ok if we keep to our simple switch/host naming
                        intfs = [ intf.link.intf1, intf.link.intf2 ]
                        intfs.remove( intf )
                        linkName = intf.name + ' ' + intfs[0].name
                        if (bool(re.search("^s.*s.*$", linkName))):
                            tcInterfaces = tcInterfaces + " " + intf.name
            info("*** Setting qos externally using TC commands from " + setTCcmd +  "\n")
            info("    on interfaces " + tcInterfaces +  "\n")
            cmd = setTCcmd + " " + tcInterfaces
            retVal = call(cmd, shell=True)
            if retVal != 0:
                info("*** error setting qos" +  "\n")
    
def throughput_H1_H2(net):
    info("*** test1 Testing Throughput between H1 and H2 (no background traffic)" +  "\n")
    info("Please wait for 30 seconds" +  "\n")
    h1 = net.getNodeByName("h1")
    h2 = net.getNodeByName("h2")
    h3 = net.getNodeByName("h3")
    h4 = net.getNodeByName("h4")
    # for udp
    #h2.cmd("iperf -s -u &")
    h2.cmd("iperf -s &")
    time.sleep(4)
    h2.cmd("ping 10.0.0.1 -c 2")
    # for udp
    #h1out = h1.cmd("iperf -c 10.0.0.2 -u -b 10M -t 30 -y c -x CDMS")
    h1out = h1.cmd("iperf -c 10.0.0.2 -t 30 -y c")
    h1out = h1out.split(",")
    if len(h1out) < 9:
        info("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)" +  "\n")
        info("***      note that these tests might fail due to the fact the network is being overloaded" +  "\n")
        info("***      you can run it again later from the command line as test1." +  "\n")
    else:
        tp=float(h1out[8])/1000000.0
        info("*** Results Throughput=" +str(tp) + "Mb/s" +  "\n")
    info("" +  "\n")

def throughput_H1_H2andH4_H3(net):
    info("*** test2 Testing Throughput between H1 and H2 with background traffic between H4 and H3" +  "\n")
    info("Please wait for 30 seconds" +  "\n")
    h1 = net.getNodeByName("h1")
    h2 = net.getNodeByName("h2")
    h3 = net.getNodeByName("h3")
    h4 = net.getNodeByName("h4")
    h2.cmd("iperf -s &")
    h3.cmd("iperf -s &")
    time.sleep(1)
    h2.cmd("ping 10.0.0.1 -c 2")
    h4.cmd("ping 10.0.0.3 -c 2")
    h1mon = h1.sendCmd("iperf -c 10.0.0.2 -t 30 -y c")
    h4out = h4.cmd("iperf -c 10.0.0.3 -t 30 -y c")
    h4out = h4out.split(",")
    if len(h4out) < 9:
        info("*** Test Failed Error, length of reply only had " + str(len(h4out)) + " field(s)" +  "\n")
        info("***      note that these tests might fail due to the fact the network is being overloaded" +  "\n")
        info("***      you can run it again later from the command line as test1." +  "\n")
    else:
        tp=float(h4out[8])/1000000.0
        info("*** Results Throughput from H4=" +str(tp) + "Mb/s" +  "\n")
    h1out= h1.waitOutput()
    h1out = h1out.split(",")
    if len(h1out) < 9:
        info("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)" +  "\n")
        info("***      note that these tests might fail due to the fact the network is being overloaded" +  "\n")
        info("***      you can run it again later from the command line as test1." +  "\n")
    else:
        tp=float(h1out[8])/1000000.0
        info("*** Results Throughput from H1=" +str(tp) + "Mb/s" +  "\n")
    info("" +  "\n")

def throughput_H1_H2andH5_H2(net):
    info("*** test3 Testing Simultaneous Throughput H1 to H2 and H5 to H2" +  "\n")
    info("Please wait for 30 seconds" +  "\n")
    h1 = net.getNodeByName("h1")
    h2 = net.getNodeByName("h2")
    h3 = net.getNodeByName("h3")
    h4 = net.getNodeByName("h4")
    h5 = net.getNodeByName("h5")
    h2.cmd("iperf -s &")
    time.sleep(1)
    h2.cmd("ping 10.0.0.1 -c 2")
    h2.cmd("ping 10.0.0.5 -c 2")
    h1mon = h1.sendCmd("iperf -c 10.0.0.2 -t 30 -y c")
    h5out = h5.cmd("iperf -c 10.0.0.2 -t 30 -y c")
    h5out = h5out.split(",")
    if len(h5out) < 9:
        info("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)" +  "\n")
        info("***      note that these tests might fail due to the fact the network is being overloaded" +  "\n")
        info("***      you can run it again later from the command line as test1." +  "\n")
    else:
        tp=float(h5out[8])/1000000.0
        info("*** Results Throughput from H5=" +str(tp) + "Mb/s" +  "\n")

    h1out= h1.waitOutput()
    h1out = h1out.split(",")
    if len(h1out) < 9:
        info("*** Test Failed Error, length of reply only had " + str(len(h1out)) + " field(s)" +  "\n")
        info("***      note that these tests might fail due to the fact the network is being overloaded" +  "\n")
        info("***      you can run it again later from the command line as test1." +  "\n")
    else:
        tp=float(h1out[8])/1000000.0
        info("*** Results Throughput from H1=" +str(tp) + "Mb/s" +  "\n")
    info("" +  "\n")

def arp_and_ping_H4_H3(net):
    info("*** test4 Ping h4 to h3 10 times (including arp at beginning)" +  "\n")
    if net.argsSdn == True:
        info("    waiting 10s for any old flow rules to flush out" +  "\n")
        # I lied, lets wait 12 seconds just in case
        time.sleep(15)
    h4 = net.getNodeByName("h4")
    h3 = net.getNodeByName("h3")
    h4.cmd("arp -d 10.0.0.3")
    h3.cmd("arp -d 10.0.0.4")
    h4.cmdPrint("ping -c 10 10.0.0.3" +  "\n")
    info("" +  "\n")

def noarp_and_ping_H4_H3(net):
    h4 = net.getNodeByName("h4")
    h4out=h4.cmd("ping -c 1 10.0.0.3")
    info("*** test5 Ping h4 to h3 10 times (no arp at beginning)" +  "\n")
    if net.argsSdn == True:
        info("    waiting 10s for any old flow rules to flush out" +  "\n")
        # I lied, lets wait 12 seconds just in case
        time.sleep(15)
    h4.cmdPrint("ping -c 10 10.0.0.3" +  "\n")
    info("" +  "\n")


#Wrappers needed for command line
def test1(self,line):
    net = self.mn
    throughput_H1_H2(net)

def test2(self,line):
    net = self.mn
    throughput_H1_H2andH4_H3(net)
    
def test3(self,line):
    net = self.mn
    throughput_H1_H2andH5_H2(net)
    
def test4(self,line):
    net = self.mn
    arp_and_ping_H4_H3(net)
    
def test5(self,line):
    net = self.mn
    noarp_and_ping_H4_H3(net)
    
    
def printSTP():
    # get the list of ports, this is nasty, but works
    ports=check_output('sudo ovs-vsctl list port | grep name | grep "-" | awk "{print \$3}" | sort',shell=True).decode('utf-8')
    # for each port
    for i in ports.splitlines():
        reply=check_output("/usr/bin/ovs-vsctl list port " + i,shell=True).decode('utf-8')
        reply=reply.replace("\n"," ")
        # again nasty
        filtered = re.sub(r'.*rstp_port_role(.*),.*$',r'\1',reply)
        info(i + filtered + "\n")
    info("")

    

if __name__ == '__main__':
    # parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--controller", help="sdn controller ip [127.0.0.1]", default="127.0.0.1")
    parser.add_argument("-p","--port", type=int, help="sdn controller port [6633]", default=6633)
    parser.add_argument("-t","--tests", action='store_true', help="run tests automatically")
    parser.add_argument("-q","--qos", action='store_true', help="configure qos outside mininet")
    group=parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--sdn", action='store_true', help="enable SDN mode (the default)")
    group.add_argument("-n", "--normal", action='store_true', help="enable STP mode (not the default)")
    args = parser.parse_args()
    if args.normal == False:
        args.sdn = True
    if args.sdn == True:
        info("Running in SDN mode" + "\n" +  "\n")
    else:
        info("Running in STP mode" +  "\n")
        
    # kill any old mininet first
    os.system("mn -c > /dev/null 2>&1")    
    setLogLevel( 'info' )
    topo = SquareTopo(args.qos)
    net = Mininet( topo=topo,
                   link=TCLink,
                   controller=None)
    net.argsSdn=args.sdn
    if args.sdn :
        net.addController( 'c0', controller=RemoteController, ip=args.controller, port=args.port )

    net.start()
    topo.afterStartConfig(net,args.sdn,args.qos)
    #print "*** Dumping host connections"
    #dumpNodeConnections(net.hosts)
    #print "*** Dumping switch connections"
    #dumpNodeConnections(net.switches)
    info("Waiting for startup and network to settle (please wait 5 seconds)" +  "\n")
    time.sleep(5)
    if args.sdn == False:
        info("*** STP state of the switches" +  "\n")
        printSTP()
        info("*** done printing STP state" +  "\n")
        info("" +  "\n")
    if args.qos == True:
        info("*** Showing Queues in s1-eth2" +  "\n")
        s1 = net.getNodeByName("s1")
        s1.cmdPrint("tc -g class show dev s1-eth2")        
    
    if args.tests == True :
        net.pingAll()
        info("" +  "\n")
        throughput_H1_H2(net)
        info("waiting 20s for the buffers to empty" +  "\n")
        time.sleep(20)
        throughput_H1_H2andH4_H3(net)
        info("waiting 20s for the buffers to empty" +  "\n")
        time.sleep(20)
        throughput_H1_H2andH5_H2(net)
        info("waiting 20s for the buffers to empty" +  "\n")
        time.sleep(20)
        arp_and_ping_H4_H3(net)
        time.sleep(10)
        noarp_and_ping_H4_H3(net)
        
    CLI.do_test1 = test1
    CLI.do_test2 = test2
    CLI.do_test3 = test3
    CLI.do_test4 = test4
    CLI.do_test5 = test5
    info("enter \"quit\" to exit or issue mininet commands if you know them" +  "\n")
    info("you can run the tests using the commands \"test1\" or \"test2\" ...." +  "\n")
    CLI(net)
    net.stop()
