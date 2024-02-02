#!/bin/bash

# Define package name and version
PKG_NAME=update-route53-ip
VERSION=1.0.0

# Install python depencencies into venv/
# This is intentionally commented out because I need to build a deb that works
# on both arm and x86_64 and python probably has some compiled binaries in these deps
#
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# deactivate

# brew install gnu-tar
# FPM needs gnu-tar or it fails, maybe I should containerize it?
rm "${PKG_NAME}_${VERSION}_all.deb"

# Build the package
fpm -s dir -t deb -n ${PKG_NAME} -v ${VERSION} \
    -a all \
    --description "Update Route53 IP service" \
    --prefix /opt/${PKG_NAME} \
    --depends python3-boto3 \
    --depends python3-requests \
    --after-install packaging/postinst.sh \
    --before-remove packaging/prerm.sh \
    --config-files packaging/config \
    ./update_route53_ip.py \
    ./systemd/${PKG_NAME}.service \
    ./packaging/config=config

    # ./venv \
