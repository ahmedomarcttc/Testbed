#!/bin/bash

# echo "Step 1: Updating & Installing make git python tox libmysqlclient-dev"
# sudo apt-get update
# sudo apt-get install -y make git python tox libmysqlclient-dev

cd
echo "Creating Folder osm and cloning openvim to install lib_osm_openvim"
if [ ! -d /home/$(whoami)/osm ]; then
	mkdir osm;
fi
cd osm
git clone https://osm.etsi.org/gerrit/osm/openvim
git -C openvim checkout 005a9dc  # this is temporal, because last version contains error at Makefile
sudo make -C openvim lite
cd
# Use this line to check if it is installed and where
sudo python -c 'import lib_osm_openvim; print lib_osm_openvim.__path__[0]'
# Install database of ovim library
OSMLIBOVIM_PATH=`python -c 'import lib_osm_openvim; print lib_osm_openvim.__path__[0]'`
# -U and -P are the admin database user/password. Normally "-U root" without password "executed as root"
sudo ${OSMLIBOVIM_PATH}/database_utils/install-db-server.sh -U root [-P passwd] -u mano -p manopw -d mano_vim_db --updatedb

echo "Cloning and installing OSM RO"
# RO (openmano)
cd osm
git clone https://osm.etsi.org/gerrit/osm/RO.git
cd RO
git checkout v2.0
sudo scripts/install-openmano.sh -u root -p root --noclone --forcedb --force --develop
cd
