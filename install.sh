sudo -- sh -c 'apt-get update; apt-get upgrade -y; apt-get dist-upgrade -y; apt-get autoremove -y; apt-get autoclean -y'
sudo apt-get install python3-pip -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
sudo curl -sS https://get.docker.com/ | sh
sudo systemctl start docker
sudo systemctl enable docker
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh)"
wget https://raw.githubusercontent.com/AmirOVH/outline-install/main/outline-install.sh
chmod +x outline-install.sh
sudo ./outline-install.sh
sudo apt-get install ufw -y
sudo ufw allow 1024:65535/tcp
sudo ufw enable
