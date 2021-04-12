#!/usr/bin/python
import os

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.topo import Topo


def _setup_environment(path_1_bw, path_1_delay, path_1_loss, path_2_bw, path_2_delay, path_2_loss, project_home_dir):
    class DoubleConnTopo(Topo):
        def build(self):
            client_host = self.addHost("client")
            server_host = self.addHost("server")
            s1_switch = self.addSwitch('s1')
            self.addLink(s1_switch, client_host, bw=path_1_bw, delay=path_1_delay, loss=path_1_loss, cls=TCLink)
            self.addLink(s1_switch, client_host, bw=path_2_bw, delay=path_2_delay, loss=path_2_loss, cls=TCLink)
            self.addLink(s1_switch, server_host, bw=(path_1_bw + path_2_bw), cls=TCLink)

    net = Mininet(topo=DoubleConnTopo(), switch=OVSBridge, controller=None, link=TCLink)
    server = net.get("server")
    client = net.get("client")
    s1 = net.get("s1")

    server.setIP("10.0.0.20", intf="server-eth0")
    client.setIP("10.0.0.1", intf="client-eth0")
    client.setIP("10.0.0.2", intf="client-eth1")

    routing_script_path = os.path.join(project_home_dir, "optimum_split_training/scripts/routing.sh")
    client.cmd("chmod +x " + routing_script_path)
    client.cmd("bash " + routing_script_path)

    net.start()

    return net


def _run_experiment(path_1_bw, path_1_delay, path_1_loss, path_2_bw, path_2_delay, path_2_loss, project_home_dir,
                    split_ratio, run_id, current_exp_dir):
    net = _setup_environment(path_1_bw, path_1_delay, path_1_loss, path_2_bw, path_2_delay, path_2_loss,
                             project_home_dir)
    scheduler = "optimum_split"
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
    server_cmd = "cd {} && ./server --scheduler={} --split_ratio={} > {} &".format(
        project_home_dir, scheduler, split_ratio, os.path.join(current_exp_dir, exp_file_name_server))

    client_cmd = "cd {} && ./client --scheduler={} --action=2 --file_name=sample.txt --split_ratio={} > {}".format(
        client_dir, scheduler, split_ratio, os.path.join(current_exp_dir, exp_file_name_client))

    client.cmd(env_variables_cmd)
    server.cmd(env_variables_cmd)

    server.cmd(server_cmd)
    client.cmd(client_cmd)

    net.stop()


def run_exp_for_combination(path_1_bw, path_1_delay, path_1_loss, path_2_bw, path_2_delay, path_2_loss, split_ratio,
                            runs_per_combination):
    setLogLevel('warning')
    project_home_dir = os.getenv("PROJECT_HOME_DIR", "/home/sharan/mpquic_ftp")
    EXPERIMENTS_DIR = os.path.join(project_home_dir, "optimum_split_training/experiments")

    current_exp_dir = os.path.join(EXPERIMENTS_DIR, str(path_1_bw) + "_" + str(path_1_delay) + "_" + str(path_1_loss) +
                                   "_" + str(path_2_bw) + "_" + str(path_2_delay) + "_" + str(path_2_loss) + "_"
                                   + str(split_ratio))
    os.makedirs(current_exp_dir, exist_ok=True)
    for i in range(0, runs_per_combination):
        _run_experiment(path_1_bw, path_1_delay, path_1_loss, path_2_bw, path_2_delay, path_2_loss, project_home_dir,
                        split_ratio, i, current_exp_dir)

