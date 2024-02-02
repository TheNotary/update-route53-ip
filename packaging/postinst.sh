#!/bin/bash

# Prompt For configuring

echo "/etc/"
read -s -p "Enter the aws secret access key (the long string): " aws_key
read -s -p "Enter the aws key_id (the short string): " aws_key_id
read -s -p "Enter the aws hosted_zone_id for the domain you'll be updating: " hosted_zone_id
read -s -p "Enter the aws domain_name for the domain you'll be updating: " domain_name

sed -i "s/{{~AWS_KEY~}}/$aws_key/g" /etc/${PKG_NAME}/config
sed -i "s/{{~AWS_KEY_ID~}}/$aws_key_id/g" /etc/${PKG_NAME}/config
sed -i "s/{{~HOSTED_ZONE_ID~}}/$hosted_zone_id/g" /etc/${PKG_NAME}/config
sed -i "s/{{~DOMAIN_NAME~}}/$domain_name/g" /etc/${PKG_NAME}/config


# Link, enable and start the systemd service
PKG_NAME=update-route53-ip

ln -s /opt/${PKG_NAME}/systemd/${PKG_NAME}.service /etc/systemd/system/${PKG_NAME}.service
systemctl daemon-reload
systemctl enable update-route53-ip.service
systemctl start update-route53-ip.service
