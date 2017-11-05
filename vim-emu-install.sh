#!/bin/bash

echo "Step 1: Updating and upgrading Ubuntu OS"
sudo apt-get update -y && sudo apt-get upgrade -y

echo "Step 2: Installing ansible and aptitude"
sudo apt-get install -y ansible git aptitude

echo "Step 3: Installing Containernet"
cd
git clone https://github.com/ahmedomarcttc/containernet.git
cd ~/containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml

echo "Step 3: Installing the emulator"
cd
git clone https://osm.etsi.org/gerrit/osm/vim-emu.git
cd ~/vim-emu/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..
#cd /home/$(whoami)/vim-emu
sudo python setup.py install

echo "Running Emulator unit tests to validate installation"
sudo py.test -v src/emuvim/test/unittests

echo "Run demo topology"
sudo python demo_topology.py
