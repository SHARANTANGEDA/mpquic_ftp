#!/usr/bin/python
import argparse
import os

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
        self.addLink(s1, client, bw=client_path_1_bw, delay=latency, cls=TCLink)
        self.addLink(s1, client, bw=client_path_2_bw, delay=latency, cls=TCLink)
        self.addLink(s1, server, bw=(client_path_1_bw + client_path_2_bw), cls=TCLink)


def setup_environment():
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

    net.start()

    return net


def run_experiment(scheduler, run_id):
    net = setup_environment()

    # Create Exp file
    exp_file_name_server = "server_" + str(run_id) + ".txt"
    exp_file_name_client = "client_" + str(run_id) + ".txt"
    server = net.get('server')
    client = net.get('client')
    s1 = net.get("s1")

    # Setup Mininet Env
    # TODO: Expose Error when the file is not present
    env_variables_cmd = "cd {} && set -a && source {} && set +a".format(project_home_dir, "envs/mininet.env")
    client_dir = os.path.join(project_home_dir, "client")
    server_cmd = "cd {} && ./server --scheduler={} > {} &".format(project_home_dir, scheduler,
                                                                  os.path.join(current_exp_dir, exp_file_name_server))

    client_cmd = "cd {} && ./client --scheduler={} --action=2 --file_name=sample.txt> {}".format(
        client_dir, scheduler, os.path.join(current_exp_dir, exp_file_name_client))

    client.cmd(env_variables_cmd)
    server.cmd(env_variables_cmd)

    server.cmd(server_cmd)
    client.cmd(client_cmd)

    net.stop()


if __name__ == '__main__':
    setLogLevel('warning')
    parser = argparse.ArgumentParser(description='Execute with Defined Bandwidth for path-1 and path-2')
    parser.add_argument('--path_1_bw', type=float, dest="path_1_bw", help="Set Bandwidth for client path 1",
                        default=10)
    parser.add_argument('--path_2_bw', type=float, dest="path_2_bw", help="Set Bandwidth for client path 2",
                        default=10)
    # parser.add_argument("--scheduler_name", type=str, dest="scheduler", help="Choose Scheduler Name")
    parser.add_argument('--latency', type=str, dest="latency", help="Set Client Delay", default='0ms')

    args = parser.parse_args()
    project_home_dir = os.getenv("PROJECT_HOME_DIR", "/home/sharan/mpquic_ftp")
    EXPERIMENTS_DIR = os.path.join(project_home_dir, "mininettest/experiments")
    client_path_1_bw, client_path_2_bw = args.path_1_bw, args.path_2_bw
    latency = args.latency

    schedulers = ["peekaboo", "ecf", "blest", "first_path"]
    total_cnt, current_cnt = 200, 0
    for scheduler in schedulers:
        for bw in [0.5, 1.0, 2.0, 5.0, 10.0]:
            client_path_1_bw = bw
            client_path_2_bw = bw
            current_exp_dir = os.path.join(EXPERIMENTS_DIR, scheduler, str(client_path_1_bw) + "_" +
                                           str(client_path_2_bw) + "_" + str(latency))
            os.makedirs(current_exp_dir, exist_ok=True)
            for i in range(0, 10):
                run_experiment(scheduler, i)
                current_cnt += 1
                print("Progress: {}/{}; {}% <==> {}".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt,
                                                            scheduler))
