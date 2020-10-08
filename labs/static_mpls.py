#!/usr/bin/env python3

from mininet.net import Containernet
from mininet.cli import CLI
from mininet.node import Intf
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet()

h1  = net.addDocker('h1',  dimage="gracious-ritchie:iperf3")
ce1 = net.addDocker('ce1', dimage="gracious-ritchie:frrouting-debian")
pe1 = net.addDocker('pe1', dimage="gracious-ritchie:frrouting-debian")
p1  = net.addDocker('p1',  dimage="gracious-ritchie:frrouting-debian")
pe2 = net.addDocker('pe2', dimage="gracious-ritchie:frrouting-debian")
ce2 = net.addDocker('ce2', dimage="gracious-ritchie:frrouting-debian")
h2  = net.addDocker('h2',  dimage="gracious-ritchie:iperf3")

net.start()

# Clean up the docker interface bullshit
for host in net.hosts:
    host.cmdPrint("ip link set dev eth0 down")

# Setup interfaces, IPs and links
net.addLink(h1,  ce1,  intfName1='h1-lan0',  intfName2='ce1-lan0', params1={'ip':'192.168.1.1/24'}, params2={'ip':'192.168.1.254/24'}, addr1="00:00:00:11:11:11", addr2="00:00:00:22:22:22")
net.addLink(ce1, pe1,  intfName1='ce1-wan0', intfName2='pe1-wan0', params1={'ip':'200.0.0.1/30' },  params2={'ip':'200.0.0.2/30'},     addr1="00:00:00:33:33:33", addr2="00:00:00:44:44:44")
net.addLink(pe1, p1,   intfName1='pe1-wan1', intfName2='p1-wan0',  params1={'ip':'200.0.1.1/30' },  params2={'ip':'200.0.1.2/30'},     addr1="00:00:00:55:55:55", addr2="00:00:00:66:66:66")
net.addLink(p1,  pe2,  intfName1='p1-wan1',  intfName2='pe2-wan1', params1={'ip':'200.0.2.1/30' },  params2={'ip':'200.0.2.2/30'},     addr1="00:00:00:77:77:77", addr2="00:00:00:88:88:88")
net.addLink(pe2, ce2,  intfName1='pe2-wan0', intfName2='ce2-wan0', params1={'ip':'200.0.3.1/30' },  params2={'ip':'200.0.3.2/30'},     addr1="00:00:00:99:99:99", addr2="00:00:00:AA:AA:AA")
net.addLink(h2,  ce2,  intfName1='h2-lan0',  intfName2='ce2-lan0', params1={'ip':'192.168.2.1/24'}, params2={'ip':'192.168.2.254/24'}, addr1="00:00:00:BB:BB:BB", addr2="00:00:00:CC:CC:CC")

# Configure hosts
h1.setDefaultRoute('via 192.168.1.254')
h2.setDefaultRoute('via 192.168.2.254')

# Configure routers
routers = [ce1, ce2, pe1, pe2, p1]
for router in routers:
    router.cmd("/etc/init.d/frr start")

    # Enable MPLS on every router's interfaces
    router.cmd("sysctl -w net.mpls.platform_labels=100000")
    for intf_name in router.intfNames():
        router.cmd(f"sysctl -w net.mpls.conf.{intf_name}.input=1")

ce1.cmd('vtysh --command "c" --command "ip route 192.168.2.0/24 200.0.0.2 label 100"')

pe1.cmd('vtysh --command "c" --command "ip route 192.168.2.0/24 200.0.0.2 label 100"')


pe1.cmd('vtysh --command "c" --command "mpls lsp 100 200.0.1.2 100"')
p1.cmd('vtysh  --command "c" --command "mpls lsp 100 200.0.2.2 100"')
pe2.cmd('vtysh --command "c" --command "mpls lsp 100 200.0.3.2 implicit-null"')

ce2.cmd('vtysh --command "c" --command "ip route 192.168.1.0/24 200.0.3.1 label 101"')
pe2.cmd('vtysh --command "c" --command "mpls lsp 101 200.0.2.1 101"')
p1.cmd('vtysh  --command "c" --command "mpls lsp 101 200.0.1.1 101"')
pe1.cmd('vtysh --command "c" --command "mpls lsp 101 200.0.0.1 implicit-null"')

CLI(net)

net.stop()