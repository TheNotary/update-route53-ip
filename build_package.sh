#!/bin/bash

# Define package name and version
PKG_NAME=update-route53-ip
VERSION=1.0.0

# Install python depencencies into venv/
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# deactivate

# brew install gnu-tar
# FPM needs gnu-tar or it fails, maybe I should containerize it?
export PATH="/usr/local/opt/gnu-tar/libexec/gnubin:$PATH"

# Build the package
fpm -s dir -t deb -n ${PKG_NAME} -v ${VERSION} \
    -a amd64 \
    --description "Update Route53 IP service" \
    --prefix /opt/${PKG_NAME} \
    --depends python3-venv \
    --depends python3-pip \
    --after-install packaging/postinst.sh \
    --before-remove packaging/prerm.sh \
    --config-files /etc/${PKG_NAME}/config \
    ./venv \
    ./update_route53_ip.py \
    ./systemd/${PKG_NAME}.service \
    ./packaging/config
    # --chdir path/to/your/project \
    # -a armhf \
