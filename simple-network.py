#!/usr/bin/python

"""
Simple example of small toplogy
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, output
from mininet.cli import CLI
import time

class SquareTopo(Topo):
    "Square switch topology with five hosts"
    def __init__(self, **opts):
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

if __name__ == '__main__':
    setLogLevel( 'info' )
    topo = SquareTopo()
    net = Mininet( topo=topo,
                   link=TCLink,
                   controller=None)
    net.addController( 'c0', controller=RemoteController, ip="127.0.0.1", port=6633 )
    net.start()
    print "*** Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "*** Dumping switch connections"
    dumpNodeConnections(net.switches)
    print("Waiting for startup and network to settle (please wait 5 seconds)")
    time.sleep(5)
    CLI(net)
    net.stop()
