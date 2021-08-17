"""
Exemple de topologie avec deux hotes et un commutateur
     -(s1)-
    |      |
(h1)    -   (h2)
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI

net = Mininet(controller=Controller)
net.addController('c0')

h1 = net.addHost(name='h1', ip='10.0.0.1/24')
h2 = net.addHost(name='h2', ip='10.0.0.2/24')

s1 = net.addSwitch('s1')

net.addLink(h1, s1)
net.addLink(h2, s1)

net.start()

CLI(net)

net.stop()
