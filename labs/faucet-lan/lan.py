from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=RemoteController)
c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
net.addController('c0')

s1 = net.addSwitch('s1', dpid='0000000000000001')

h1 = net.addHost('h1', ip='10.10.10.1')
h2 = net.addHost('h2', ip='20.20.20.1')
h3 = net.addHost('h3', ip='30.30.30.1')

net.addLink(s1, h1, port1=1, port2=1)
net.addLink(s1, h2, port1=2, port2=1)
net.addLink(s1, h3, port1=3, port2=1)

net.start()

h1.setDefaultRoute('via 10.10.10.254')
h2.setDefaultRoute('via 20.20.20.254')
h3.setDefaultRoute('via 30.30.30.254')

CLI(net)

net.stop()
