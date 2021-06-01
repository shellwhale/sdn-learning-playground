#!/usr/bin/env python3

from mininet.net import Containernet
from mininet.cli import CLI
from mininet.node import Intf
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet()
net.addController('c0')

r1 = net.addDocker('r1', dimage="gracious-ritchie/labs/bgp/frrouting:latest")
r2 = net.addDocker('r2', dimage="gracious-ritchie/labs/bgp/frrouting:latest")
r3 = net.addDocker('r3', dimage="gracious-ritchie/labs/bgp/frrouting:latest")
r4 = net.addDocker('r4', dimage="gracious-ritchie/labs/bgp/frrouting:latest")
routers = [r1, r2, r3, r4]

h1 = net.addDocker('h1', dimage="gracious-ritchie:iperf3")
h2 = net.addDocker('h2', dimage="gracious-ritchie:iperf3")
h3 = net.addDocker('h3', dimage="gracious-ritchie:iperf3")
h4 = net.addDocker('h4', dimage="gracious-ritchie:iperf3")
hosts = [h1, h2, h3, h4]

s1 = net.addSwitch('s1')

net.start()

net.addLink(r1, s1, intfName1='r1-wan0', params1={'ip':'200.0.0.1/24'})
net.addLink(r2, s1, intfName1='r2-wan0', params1={'ip':'200.0.0.2/24'})
net.addLink(r3, s1, intfName1='r3-wan0', params1={'ip':'200.0.0.3/24'})

# net.addLink(r3, s1, intfName1='r3-wan1', params1={'ip':'95.86.34.3/24'})
# net.addLink(r4, s1, intfName1='r4-wan0', params1={'ip':'95.86.34.4/24'})


# net.addLink(r3, s1, intfName1='r3-wan1', params1={'ip':'95.86.34.3/24'})
# net.addLink(r4, s1, intfName1='r4-wan0', params1={'ip':'95.86.34.4/24'})

net.addLink(r3,  r4,  intfName1='r3-to-r4',  intfName2='r4-to-r3', params1={'ip':'95.86.34.3/24'}, params2={'ip':'95.86.34.4/24'})

net.addLink(h1,  r1,  intfName1='h1-lan0',  intfName2='r1-lan0', params1={'ip':'192.168.1.1/24'}, params2={'ip':'192.168.1.254/24'})
net.addLink(h2,  r2,  intfName1='h2-lan0',  intfName2='r2-lan0', params1={'ip':'192.168.2.1/24'}, params2={'ip':'192.168.2.254/24'})
net.addLink(h3,  r3,  intfName1='h3-lan0',  intfName2='r3-lan0', params1={'ip':'192.168.3.1/24'}, params2={'ip':'192.168.3.254/24'})
net.addLink(h4,  r4,  intfName1='h4-lan0',  intfName2='r4-lan0', params1={'ip':'192.168.4.1/24'}, params2={'ip':'192.168.4.254/24'})

# Give time to the user to run Wireshark
input("Press enter to start")

# Configure hosts
h1.setDefaultRoute('via 192.168.1.254')
h2.setDefaultRoute('via 192.168.2.254')
h3.setDefaultRoute('via 192.168.3.254')
h4.setDefaultRoute('via 192.168.4.254')

# Configure routers
for router in routers:
    router.cmd("/etc/init.d/frr start")

# Configure subnets to advertise
r1.cmd('vtysh --command "c" --command "router bgp 100" --command "network 192.168.1.0/24"')
r2.cmd('vtysh --command "c" --command "router bgp 200" --command "network 192.168.2.0/24"')
r3.cmd('vtysh --command "c" --command "router bgp 300" --command "network 192.168.3.0/24"')
r4.cmd('vtysh --command "c" --command "router bgp 400" --command "network 192.168.4.0/24"')

# Configure neighbors
r1.cmd('vtysh --command "c" --command "router bgp 100" --command "neighbor 200.0.0.2 remote-as 200"')
r1.cmd('vtysh --command "c" --command "router bgp 100" --command "neighbor 200.0.0.3 remote-as 300"')

r2.cmd('vtysh --command "c" --command "router bgp 200" --command "neighbor 200.0.0.1 remote-as 100"')
r2.cmd('vtysh --command "c" --command "router bgp 200" --command "neighbor 200.0.0.3 remote-as 300"')

r3.cmd('vtysh --command "c" --command "router bgp 300" --command "neighbor 200.0.0.1 remote-as 100"')
r3.cmd('vtysh --command "c" --command "router bgp 300" --command "neighbor 200.0.0.2 remote-as 200"')
r3.cmd('vtysh --command "c" --command "router bgp 300" --command "neighbor 95.86.34.4 remote-as 400"')

r4.cmd('vtysh --command "c" --command "router bgp 400" --command "neighbor 95.86.34.3 remote-as 300"')



# Clean up the docker interface bullshit
for host in net.hosts:
    host.cmdPrint("ip link set dev eth0 down")

CLI(net)

net.stop()