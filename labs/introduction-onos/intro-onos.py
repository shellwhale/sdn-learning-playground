"""
     -(s1)-
    |      |
(s2)    -   (s3)
 |            |
(h1)        (h2)

"""
from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=RemoteController)
c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
net.addController('c0')

h1 = net.addHost('h1', ip='10.0.0.1/24')
h2 = net.addHost('h2', ip='10.0.0.2/24')

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

net.addLink(s1, s2)
net.addLink(s1, s3)

net.addLink(s2, h1)
net.addLink(s3, h2)

net.start()

CLI(net)

net.stop()
