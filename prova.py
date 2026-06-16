####################################
#   Nome: Joao Victor Nascimento   #
####################################
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

def configure_network():
    net = Mininet(link=TCLink, controller=None)

    #lan-2
    d1 = net.addHost('d1', ip='172.16.2.1/24', defaultRoute='via 172.16.2.254')
    d2 = net.addHost('d2', ip='172.16.2.2/24', defaultRoute='via 172.16.2.254')
    d3 = net.addHost('d3', ip='172.16.2.3/24', defaultRoute='via 172.16.2.254')
    d4 = net.addHost('d4', ip='172.16.2.4/24', defaultRoute='via 172.16.2.254')
    d5 = net.addHost('d5', ip='172.16.2.5/24', defaultRoute='via 172.16.2.254')

    #lan-3
    a1 = net.addHost('a1', ip='172.16.3.1/24', defaultRoute='via 172.16.3.254')
    a2 = net.addHost('a2', ip='172.16.3.2/24', defaultRoute='via 172.16.3.254')
    a3 = net.addHost('a3', ip='172.16.3.3/24', defaultRoute='via 172.16.3.254')
    a4 = net.addHost('a4', ip='172.16.3.4/24', defaultRoute='via 172.16.3.254')
    a5 = net.addHost('a5', ip='172.16.3.5/24', defaultRoute='via 172.16.3.254')
    
    #roteador
    r1 = net.addHost('r1', cls=LinuxRouter,  ip='172.16.2.254/24')

    #switch's
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')

    #links
    net.addLink(d1, s1)
    net.addLink(d2, s1)
    net.addLink(d3, s1)
    net.addLink(d4, s1)
    net.addLink(d5, s1)

    net.addLink(a1, s2)
    net.addLink(a2, s2)
    net.addLink(a3, s2)
    net.addLink(a4, s2)
    net.addLink(a5, s2)

    net.addLink(s1, r1)
    net.addLink(s2, r1)

    net.start()

    r1.cmd('ifconfig r1-eth0 172.16.2.254/24')
    r1.cmd('ifconfig r1-eth1 172.16.3.254/24')

    net.pingAll()
    CLI(net)
    net.stop()

def main():
    setLogLevel('info')
    configure_network()

main()