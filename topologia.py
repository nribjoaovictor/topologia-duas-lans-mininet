from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topologia():
    net = Mininet(controller=None, link=TCLink)

    pc1 = net.addHost('pc1', ip = '192.168.1.10/24', defaultRoute='via 192.168.1.1')
    pc2 = net.addHost('pc2', ip = '192.168.1.20/24', defaultRoute='via 192.168.1.1')

    impressora = net.addHost('impressora', ip = '192.168.1.30/24', defaultRoute='via 192.168.1.1')

    pc3 = net.addHost('pc3', ip = '192.168.2.10/24', defaultRoute='via 192.168.2.1')
    pc4 = net.addHost('pc4', ip = '192.168.2.20/24', defaultRoute='via 192.168.2.1')

    servidor = net.addHost('servidor', ip = '192.168.2.30/24', defaultRoute='via 192.168.2.1')

    print("roteador")
    router = net.addHost('r1')

    print('switches')

    sw1 = net.addSwitch('s1', failMode='standalone')
    sw2 = net.addSwitch('s2', failMode='standalone')

    print('links')
    net.addLink(pc1,sw1)
    net.addLink(pc2,sw1)
    net.addLink(impressora,sw1)

    net.addLink(pc3,sw2)
    net.addLink(pc4,sw2)
    net.addLink(servidor,sw2)

    net.addLink(router,sw1)
    net.addLink(router,sw2)

    net.start()

    print("*** Configurando roteador")

    router.cmd('ifconfig r1-eth0 192.168.1.1/24')
    router.cmd('ifconfig r1-eth1 192.168.2.1/24')

    router.cmd('sysctl -w net.ipv4.ip_forward=1')

    print("*** Topologia pronta")

    CLI(net)

    net.stop()

def main():
    setLogLevel('info')
    topologia()
main()