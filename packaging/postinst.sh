#!/bin/bash

PKG_NAME=update-route53-ip

# I don't like this because I don't want credentials floating around after I uninstall this...
# Setup AWS Secrets
# [ -f "${HOME}/.aws" ] || mkdir "${HOME}/.aws"
#
# config_file="${HOME}/.aws/config"
# if [ ! -f "${config_file}" ]; then
#   printf "[default]\nregion = us-west-1\n" | tee -a "${config_file}" > /dev/null
# else
#   echo "Config file already exists at ${config_file}.  Skipping."
# fi

# credential_file="${HOME}/.aws/credentials"
# if [ ! -f "${credential_file}" ]; then
#   echo "The aws_terraform project produces credentials with limited access to just route53 resources named automated_tf."
#   read -s -p "Enter the aws secret access key (the long string): " key
#   read -s -p "Enter the aws key_id (the short string): " key_id
#   printf "[default]\naws_secret_access_key = ${key}\naws_access_key_id = ${key_id}" | tee -a "${credential_file}" > /dev/null
# else
#   echo "Credential file already exists at ${credential_file}.  Skipping."
# fi

echo "Creating service account"
getent passwd updateroute53ipsa > /dev/null || useradd -r -s /usr/sbin/nologin updateroute53ipsa

config_path="/opt/${PKG_NAME}/config"

echo "Populating ${config_path}"
read -s -p "Enter the aws secret access key (the long string): " aws_key
echo ""
read -s -p "Enter the aws key_id (the short string): " aws_key_id
echo ""
read -p "Enter the aws hosted_zone_id for the domain you'll be updating: " hosted_zone_id
read -p "Enter the aws domain_name for the domain you'll be updating: " domain_name

sed -i "s/~AWS_KEY~/${aws_key}/g" ${config_path}
sed -i "s/~AWS_KEY_ID~/${aws_key_id}/g" ${config_path}
sed -i "s/~HOSTED_ZONE_ID~/${hosted_zone_id}/g" ${config_path}
sed -i "s/~DOMAIN_NAME~/${domain_name}/g" ${config_path}

chmod 0640 ${config_path}
chgrp updateroute53ipsa ${config_path}
chgrp -R updateroute53ipsa /opt/${PKG_NAME}

# Link, enable and start the systemd service
ln -s /opt/${PKG_NAME}/systemd/${PKG_NAME}.service /etc/systemd/system/${PKG_NAME}.service
systemctl daemon-reload
systemctl enable update-route53-ip.service
systemctl start update-route53-ip.service

echo ""
echo "Congratulations!"
echo "update-route53-ip service should now be running."
echo "  To verify it's running and not in a reboot loop, run:"
echo "systemctl status update-route53-ip.service"
echo "  To view the logs, run:"
echo "journalctl -u update-route53-ip.service"
