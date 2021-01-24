#!/usr/bin/python
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import OVSBridge


BASIC_DELAY = 40

class DoubleConnTopo(Topo):
    def build(self):
        client = self.addHost("client")
        server = self.addHost("server")
        s1 = self.addSwitch('s1')
        self.addLink(s1, client)
        self.addLink(s1, client)
        self.addLink(s1, server)


def setup_environment():
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge, controller=None)
    server = net.get("server")
    client = net.get("client")
    s1 = net.get("s1")

    server.setIP("10.0.0.20", intf="server-eth0")
    client.setIP("10.0.0.1", intf="client-eth0")
    client.setIP("10.0.0.2", intf="client-eth1")

    client.cmd("./scripts/routing.sh")
    client.cmd("./scripts/tc_client.sh")
    s1.cmd("./scripts/tc_s1.sh")
    net.start()

    return net


def run_experiment():
    net = setup_environment()

    server = net.get('server')
    client = net.get('client')
    s1 = net.get("s1")

    s1.cmd("./scripts/set_delay.sh %d" % int(BASIC_DELAY / 2))
    client.cmd("./scripts/client_set_delay.sh %d" % int(BASIC_DELAY / 2))

    # you may want to start wireshark here and finish by typing exit
    cli = CLI(net)

    CLI.do_xterm(cli, 'server client')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('warning')
    run_experiment()


class StaticTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(h1, s1, bw=100, delay="40ms")
        self.addLink(h2, s1, bw=100)
        self.addLink(h1, s2, bw=100, delay="20ms")
        self.addLink(h2, s2, bw=100)
