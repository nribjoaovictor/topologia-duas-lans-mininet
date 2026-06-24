#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class MyTopo(Topo):
    def build(self):

        # Switches
        SDMZ = self.addSwitch('SDMZ', dpid='0000000000000001')
        s1 = self.addSwitch('s1', dpid='0000000000000002')
        s2 = self.addSwitch('s2', dpid='0000000000000003')
        s3 = self.addSwitch('s3', dpid='0000000000000004')

        # Hosts
        CE = self.addHost('CE', ip='172.17.0.10/12', defaultRoute='via 172.17.0.1')

        c1 = self.addHost('c1', ip='192.168.117.10/24', defaultRoute='via 192.168.117.1')
        c2 = self.addHost('c2', ip='192.168.117.11/24', defaultRoute='via 192.168.117.1')
        c3 = self.addHost('c3', ip='192.168.117.12/24', defaultRoute='via 192.168.117.1')
        c4 = self.addHost('c4', ip='192.168.117.13/24', defaultRoute='via 192.168.117.1')
        c5 = self.addHost('c5', ip='192.168.117.14/24', defaultRoute='via 192.168.117.1')

        servidorSSH  = self.addHost('servidorSSH', ip='192.168.26.10/24', defaultRoute='via 192.168.26.1')
        servidorFTP  = self.addHost('servidorFTP', ip='192.168.26.20/24', defaultRoute='via 192.168.26.1')
        estoqueAPI = self.addHost('estoqueAPI', ip='192.168.26.30/24', defaultRoute='via 192.168.26.1')

        servidorMongoDB  = self.addHost('servidorMongoDB', ip='192.168.48.10/24', defaultRoute='via 192.168.48.1')

        # Firewall e roteadores
        FW = self.addNode('FW', cls=LinuxRouter)
        R1 = self.addNode('R1', cls=LinuxRouter)
        R2 = self.addNode('R2', cls=LinuxRouter)
        R3 = self.addNode('R3', cls=LinuxRouter)

        # DMZ
        self.addLink(CE, SDMZ)
        self.addLink(SDMZ, FW, intfName2='FW-dmz', params2={'ip': '172.17.0.1/12'})

        # Rede clientes internos
        self.addLink(FW, s1, intfName1='FW-lan', params1={'ip': '192.168.117.254/24'})
        self.addLink(s1, c1)
        self.addLink(s1, c2)
        self.addLink(s1, c3)
        self.addLink(s1, c4)
        self.addLink(s1, c5)
        self.addLink(s1, R1, intfName2='R1-clientes', params2={'ip': '192.168.117.1/24'})

        # Rede serviços
        self.addLink(R2, s2, intfName1='R2-servicos', params1={'ip': '192.168.26.1/24'})
        self.addLink(servidorSSH, s2, intfName1='ssh0')
        self.addLink(servidorFTP, s2, intfName1='ftp0')
        self.addLink(estoqueAPI, s2, intfName1='api0')

        # Rede banco de dados
        self.addLink(R3, s3, intfName1='R3-db', params1={'ip': '192.168.48.1/24'})
        self.addLink(servidorMongoDB, s3, intfName1='mongo0')
        # Links entre roteadores
        self.addLink(
            R1, R2,
            intfName1='R1-R2', params1={'ip': '10.1.0.1/16'},
            intfName2='R2-R1', params2={'ip': '10.1.0.2/16'}
        )

        self.addLink(
            R1, R3,
            intfName1='R1-R3', params1={'ip': '10.6.0.1/16'},
            intfName2='R3-R1', params2={'ip': '10.6.0.2/16'}
        )

        self.addLink(
            R2, R3,
            intfName1='R2-R3', params1={'ip': '10.9.0.1/16'},
            intfName2='R3-R2', params2={'ip': '10.9.0.2/16'}
        )


def configurar_rotas(net):
    FW = net.get('FW')
    R1 = net.get('R1')
    R2 = net.get('R2')
    R3 = net.get('R3')

    # FW conhece redes internas por R1
    FW.cmd('ip route add 192.168.26.0/24 via 192.168.117.1')
    FW.cmd('ip route add 192.168.48.0/24 via 192.168.117.1')

    # R1 conhece DMZ, serviços e banco
    R1.cmd('ip route add 172.16.0.0/12 via 192.168.117.254')
    R1.cmd('ip route add 192.168.26.0/24 via 10.1.0.2')
    R1.cmd('ip route add 192.168.48.0/24 via 10.6.0.2')

    # R2 conhece DMZ, clientes e banco
    R2.cmd('ip route add 172.16.0.0/12 via 10.1.0.1')
    R2.cmd('ip route add 192.168.117.0/24 via 10.1.0.1')
    R2.cmd('ip route add 192.168.48.0/24 via 10.9.0.2')

    # R3 conhece DMZ, clientes e serviços
    R3.cmd('ip route add 172.16.0.0/12 via 10.6.0.1')
    R3.cmd('ip route add 192.168.117.0/24 via 10.6.0.1')
    R3.cmd('ip route add 192.168.26.0/24 via 10.9.0.1')

def iniciar_servicos(net):
    servidorSSH = net.get('servidorSSH')
    servidorFTP = net.get('servidorFTP')
    estoqueAPI = net.get('estoqueAPI')

    # SSH
    servidorSSH.cmd('ssh-keygen -A')
    servidorSSH.cmd('/usr/sbin/sshd -D &')

    # FTP simples usando pyftpdlib
    servidorFTP.cmd('mkdir -p /tmp/ftp')
    servidorFTP.cmd('python3 -m pyftpdlib -i 192.168.26.20 -p 21 -w -d /tmp/ftp &')

    # API Flask
    estoqueAPI.cmd('python3 /home/mininet/trabalho_mininet/api_estoque.py &')


def configurar_firewall(net):
    FW = net.get('FW')

    # Limpa regras anteriores
    FW.cmd('iptables -F')
    FW.cmd('iptables -t nat -F')
    FW.cmd('iptables -P FORWARD DROP')

    # Permite conexões já estabelecidas
    FW.cmd('iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT')

    # Permite CE acessar SSH
    FW.cmd('iptables -A FORWARD -s 172.17.0.10 -d 192.168.26.10 -p tcp --dport 22 -j ACCEPT')

    # Permite CE acessar FTP
    FW.cmd('iptables -A FORWARD -s 172.17.0.10 -d 192.168.26.20 -p tcp --dport 21 -j ACCEPT')

    # Permite CE acessar API Flask
    FW.cmd('iptables -A FORWARD -s 172.17.0.10 -d 192.168.26.30 -p tcp --dport 5000 -j ACCEPT')

    # Bloqueia ping vindo da DMZ para rede interna
    FW.cmd('iptables -A FORWARD -s 172.17.0.10 -p icmp -j DROP')

    # Bloqueia clientes internos acessando rede de serviços
    FW.cmd('iptables -A FORWARD -s 192.168.117.0/24 -d 192.168.26.0/24 -j DROP')

    # Bloqueia acesso direto ao banco
    FW.cmd('iptables -A FORWARD -s 172.17.0.10 -d 192.168.48.10 -j DROP')

    R1 = net.get('R1')
    R2 = net.get('R2')
    R3 = net.get('R3')
    R1.cmd('iptables -F')
    R2.cmd('iptables -F')
    R3.cmd('iptables -F')

    R1.cmd('iptables -P FORWARD ACCEPT')
    R2.cmd('iptables -P FORWARD ACCEPT')
    R3.cmd('iptables -P FORWARD ACCEPT')

    # Bloqueia clientes internos acessando rede de serviços
    R1.cmd('iptables -A FORWARD -s 192.168.117.0/24 -d 192.168.26.0/24 -j DROP')
    R2.cmd('iptables -A FORWARD -s 192.168.117.0/24 -d 192.168.26.0/24 -j DROP')

    # Bloqueia clientes internos acessando banco
    R1.cmd('iptables -A FORWARD -s 192.168.117.0/24 -d 192.168.48.0/24 -j DROP')
    R3.cmd('iptables -A FORWARD -s 192.168.117.0/24 -d 192.168.48.0/24 -j DROP')

def main():
    topo = MyTopo()
    net = Mininet(topo=topo)

    net.start()

    R1 = net.get('R1')
    R2 = net.get('R2')
    R3 = net.get('R3')
    FW = net.get('FW')

    # LAN Clientes
    R1.cmd('ip addr flush dev R1-clientes')
    R1.cmd('ip addr add 192.168.117.1/24 dev R1-clientes')

    # LAN Serviços
    R2.cmd('ip addr flush dev R2-servicos')
    R2.cmd('ip addr add 192.168.26.1/24 dev R2-servicos')

    # LAN Banco
    R3.cmd('ip addr flush dev R3-db')
    R3.cmd('ip addr add 192.168.48.1/24 dev R3-db')

    # Firewall
    FW.cmd('ip addr flush dev FW-lan')
    FW.cmd('ip addr add 192.168.117.254/24 dev FW-lan')

    FW.cmd('ip addr flush dev FW-dmz')
    FW.cmd('ip addr add 172.17.0.1/12 dev FW-dmz')

    configurar_rotas(net)
    iniciar_servicos(net)
    configurar_firewall(net)

    info('\n*** Topologia iniciada com sucesso!\n')
    info('*** Comandos úteis: nodes | net | dump | pingall\n\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()