"""
Exemple de topologie avec deux hotes et un commutateur, SANS CONTROLLEUR
     -(s1)-
    |      |
(h1)    -   (h2)
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI

net = Mininet(controller=None)

h1 = net.addHost(name='h1', ip='10.0.0.1/24', mac='00:00:00:11:11:11')
h2 = net.addHost(name='h2', ip='10.0.0.2/24', mac='00:00:00:22:22:22')
h3 = net.addHost(name='h3', ip='10.0.0.3/24', mac='00:00:00:33:33:33')

s1 = net.addSwitch('s1')

net.addLink(h1, s1)
net.addLink(h2, s1)
net.addLink(h3, s1)

net.start()

CLI(net)

net.stop()
