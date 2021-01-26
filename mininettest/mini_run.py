#!/usr/bin/python
import argparse

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.topo import Topo

BASIC_DELAY = 40

class DoubleConnTopo(Topo):
    def build(self):
        client = self.addHost("client")
        server = self.addHost("server")
        s1 = self.addSwitch('s1')
        self.addLink(s1, client)
        self.addLink(s1, client)
        self.addLink(s1, server)


def setup_environment(client_delay, switch_delay):
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge, controller=None)
    server = net.get("server")
    client = net.get("client")
    s1 = net.get("s1")

    server.setIP("10.0.0.20", intf="server-eth0")
    client.setIP("10.0.0.1", intf="client-eth0")
    client.setIP("10.0.0.2", intf="client-eth1")

    client.cmd("./scripts/routing.sh")
    if client_delay:
        client.cmd("./scripts/tc_client.sh")
    if switch_delay:
        s1.cmd("./scripts/tc_s1.sh")

    net.start()

    return net


def run_experiment(client_delay, switch_delay):
    net = setup_environment(client_delay, switch_delay)

    server = net.get('server')
    client = net.get('client')
    s1 = net.get("s1")

    if switch_delay:
        s1.cmd("./scripts/set_delay.sh %d" % int(BASIC_DELAY / 2))
    if client_delay:
        client.cmd("./scripts/client_set_delay.sh %d" % int(BASIC_DELAY / 2))

    # you may want to start wireshark here and finish by typing exit
    cli = CLI(net)

    CLI.do_xterm(cli, 'server client')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('warning')
    parser = argparse.ArgumentParser(description='Execute with defined Delay')
    parser.add_argument('--add_client_delay', type=bool, dest="client_delay", help="Set Client Delay", default=False)
    parser.add_argument('--add_switch_delay', type=bool, dest="switch_delay", help="Set Switch Delay", default=False)

    args = parser.parse_args()
    run_experiment(args.client_delay, args.switch_delay)


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
