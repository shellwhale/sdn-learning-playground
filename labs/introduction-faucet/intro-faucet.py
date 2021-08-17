from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=RemoteController)
c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
net.addController('c0')

h1 = net.addHost('h1')
h2 = net.addHost('h2')

s1 = net.addSwitch('s1', dpid='0000000000000001')

net.start()

net.addLink(s1, h1)
net.addLink(s1, h2)

CLI(net)

net.stop()
