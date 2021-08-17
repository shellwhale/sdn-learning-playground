# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"
  config.vm.hostname = "sdn-learning-playground"
  config.vm.define "sdn-learning-playground"
  config.vm.synced_folder  ".", "/vagrant", disabled: false, create: true
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive

    sudo apt-get update
    sudo apt-get install ansible git aptitude python3 iperf3 jq libjq1 libonig4 -y
    sudo apt-get install -y < /vagrant/packages.txt

    git clone https://github.com/containernet/containernet.git
    cd containernet/ansible
    sudo ansible-playbook -i "localhost," -c local install.yml
    cd ..
    sudo make develop
    sudo apt-get install docker-compose -y
    echo "cd /vagrant" >> /home/vagrant/.bashrc

    git clone https://github.com/shellwhale/iperf3_plotter
    cd iperf3_plotter
    sudo make

    sudo apt-get remove iperf3 libiperf0 -y
    sudo apt-get install libsctp1 -y
    wget https://iperf.fr/download/ubuntu/libiperf0_3.9-1_amd64.deb
    wget https://iperf.fr/download/ubuntu/iperf3_3.9-1_amd64.deb
    sudo dpkg -i libiperf0_3.9-1_amd64.deb iperf3_3.9-1_amd64.deb
    rm libiperf0_3.9-1_amd64.deb iperf3_3.9-1_amd64.deb

    sudo docker pull onosproject/onos:latest
    sudo docker pull faucet/faucet:latest
  SHELL
end
