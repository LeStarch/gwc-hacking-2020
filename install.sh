#!/usr/bin/env sh

USER=`whoami`
GITHUB_LOCATION="https://github.com/LeStarch/gwc-hacking-2020"
INSTALL_LOCATION="/opt/gwc-hacking"

NGINX_CONFIG="/etc/nginx/sites-enabled"
SYSTEMD_CONFIG="/etc/systemd/system/multi-user.target.wants"
SYSTEMD_LIB_CONFIG="/lib/systemd/system"

#Install needed apt packages
sudo apt install -y nginx python3 python3-venv build-essential git

# Setup structure if possible

# Clone the directory, if possible
if [ ! -d "${INSTALL_LOCATION}" ]
then
    sudo mkdir -p /opt
    sudo git clone "${GITHUB_LOCATION}" "${INSTALL_LOCATION}"
    sudo chown "${USER}:${USER}" "${INSTALL_LOCATION}"
fi
if [ ! -d "${INSTALL_LOCATION}/venv" ]
then
    python3 -m venv "${INSTALL_LOCATION}/venv"
fi
# Setup virtual environment
. "${INSTALL_LOCATION}/venv/bin/activate"
pip install -r "${INSTALL_LOCATION}/requirements.txt"

# Link in system setup
sudo rm -f "${NGINX_CONFIG}/default"
sudo ln -sf "${INSTALL_LOCATION}/static" "/var/www/html/gwc/static"


# Enable all services
for service in "dos-flask" "monitor"
do
    sudo ln -sf "${INSTALL_LOCATION}/config/${service}.service" "${SYSTEMD_CONFIG}/"
    sudo ln -sf "${INSTALL_LOCATION}/config/${service}.service" "${SYSTEMD_LIB_CONFIG}/"
    sudo systemctl daemon-reload
    sudo service "${service}" restart
done
