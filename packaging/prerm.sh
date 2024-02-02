#!/bin/bash
# Stop and disable the systemd service
systemctl stop update-route53-ip.service
systemctl disable update-route53-ip.service
