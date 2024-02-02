#!/usr/bin/env bash

echo "This install script is meant to be used on a RPI, or at least a debian based OS."
echo "Run as the normal user."

echo "Please input the local user's sudo password if/ when prompted" && sudo true || exit

#
# Setup for local development
#

# Install system dependencies
sudo apt-get install -y python3-boto3 python3-requests awscli

# Install python depencencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#
# Setup AWS CLI
#

[ -f "${HOME}/.aws" ] || mkdir "${HOME}/.aws"

config_file="${HOME}/.aws/config"
if [ ! -f "${config_file}" ]; then
  printf "[default]\nregion = us-west-1\n" | tee -a "${config_file}" > /dev/null
else
  echo "Config file already exists at ${config_file}.  Skipping."
fi

credential_file="${HOME}/.aws/config"
if [ ! -f "${credential_file}" ]; then
  echo "The aws_terraform project produces credentials with limited access to just route53 resources named automated_tf."
  read -s -p "Enter the aws secret access key (the long string): " key
  read -s -p "Enter the aws key_id (the short string): " key_id
  printf "[default]\naws_secret_access_key = ${key}\naws_access_key_id = ${key_id}" | tee -a "${credential_file}" > /dev/null
else
  echo "Credential file already exists at ${credential_file}.  Skipping."
fi

#
# Install systemd unit
#

systemd_file="/etc/systemd/system/update-route53-ip.service"
template_file="systemd/update-route53-ip.service"
if [ ! -f "${systemd_file}" ]; then
  sed "s/{{USERNAME}}/$current_user/g" ${template_file} | sudo tee ${systemd_file} > /dev/null
fi

sudo systemctl daemon-reload
sudo systemctl enable update-route53-ip.service
sudo systemctl start update-route53-ip.service

echo "update-route53-ip service should now be running."
echo "To verify it's running and not in a reboot loop, run:"
echo "  systemctl status update-route53-ip.service to "
echo "To view the logs, run: "
echo "  journalctl -u update-route53-ip.service "
