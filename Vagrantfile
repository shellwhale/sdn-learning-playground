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
    sudo apt update
    sudo apt-get install ansible git aptitude python3 -y
    git clone https://github.com/containernet/containernet.git
    cd containernet/ansible
    sudo ansible-playbook -i "localhost," -c local install.yml
    cd ..
    sudo make develop
    sudo apt-get install docker-compose -y
    echo "cd /vagrant" >> /home/vagrant/.bashrc
  SHELL
end
