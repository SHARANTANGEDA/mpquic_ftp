#!/usr/bin/python
import argparse
import os

from mininet.cli import CLI
from mininet.link import TCLink
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
        self.addLink(s1, client, bw=client_path_1_bw, cls=TCLink)
        self.addLink(s1, client, bw=client_path_2_bw, cls=TCLink)
        self.addLink(s1, server, bw=(client_path_1_bw+client_path_2_bw), cls=TCLink)


def setup_environment(client_delay, switch_delay):
    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge, controller=None, link=TCLink)
    server = net.get("server")
    client = net.get("client")
    s1 = net.get("s1")

    server.setIP("10.0.0.20", intf="server-eth0")
    client.setIP("10.0.0.1", intf="client-eth0")
    client.setIP("10.0.0.2", intf="client-eth1")

    routing_script_path = os.path.join(project_home_dir, "mininettest/scripts/routing.sh")
    client.cmd("chmod +x " + routing_script_path)
    client.cmd("bash " + routing_script_path)
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

    if switch_delay and project_home_dir != ".":
        delay_file_path = os.path.join(project_home_dir, "mininettest/scripts/set_delay.sh")
        s1.cmd("chmod +x " + delay_file_path)
        s1.cmd("bash " + delay_file_path + " %d" % int(BASIC_DELAY / 2))
    if client_delay and project_home_dir != ".":
        client_delay_file_path = os.path.join(project_home_dir, "mininettest/scripts/client_set_delay.sh")
        client.cmd("chmod +x " + client_delay_file_path)
        client.cmd("bash " + client_delay_file_path + " %d" % int(BASIC_DELAY / 2))

    # Setup Mininet Env
    # TODO: Expose Error when the file is not present
    env_variables_cmd = "set -a && source " + os.path.join(project_home_dir, "envs/mininet.env") + " && set +a"
    client.cmd(env_variables_cmd)
    server.cmd(env_variables_cmd)

    # you may want to start wireshark here and press exit to continue
    cli = CLI(net)

    CLI.do_xterm(cli, 'server client')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('warning')
    parser = argparse.ArgumentParser(description='Execute with Defined Bandwidth for path-1 and path-2')
    parser.add_argument('--add_client_delay', type=bool, dest="client_delay", help="Set Client Delay", default=False)
    parser.add_argument('--add_switch_delay', type=bool, dest="switch_delay", help="Set Switch Delay", default=False)
    parser.add_argument('--path_1_bw', type=int, dest="path_1_bw", help="Set Bandwidth for client path 1",
                        default=10)
    parser.add_argument('--path_2_bw', type=int, dest="path_2_bw", help="Set Bandwidth for client path 2",
                        default=10)

    args = parser.parse_args()
    project_home_dir = os.getenv("PROJECT_HOME_DIR", ".")
    client_path_1_bw, client_path_2_bw = args.path_1_bw, args.path_2_bw
    run_experiment(args.client_delay, args.switch_delay)

