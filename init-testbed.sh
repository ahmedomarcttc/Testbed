#!/bin/bash

# mysql install needs some extra tricks
echo "mysql trick config"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password root"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password root"

# updates and general box setup
echo "general setup"
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y git ansible aptitude make tox mysql-server libmysqlclient-dev
sudo apt-get install -y python python-pip python3 python3-pip
sudo echo "localhost ansible_connection=local" >> /etc/ansible/hosts

# install OpenStack client
echo "installing OpenStack client"
sudo pip3 install python-openstackclient
sudo pip3 install python-heatclient
sudo pip3 install python-neutronclient

cd /home/$(whoami)
sh $(whoami)/scripts/vim-emu-install.sh

# cd /home/$(whoami)
# sh $(whoami)/scripts/install_son-cli.sh

cd /home/$(whoami)
sh $(whoami)/scripts/install_osm_RO.sh

# cd /home/$(whoami)/vnfs
# sudo ./build.sh
