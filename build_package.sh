#!/bin/bash

# PKG_NAME='example-package'
# VERSION='1.0.0'
# VERSION='1.0.0+21AF26D3'
# ARCHITECTURE='all' # armv6l, all or x86_64
# DESCRIPTION='This is an example package'

PACKAGE_NAME="${PKG_NAME}_${VERSION}_${ARCHITECTURE}.deb"

echo "BUILDING PACKAGE: ${PACKAGE_NAME}"

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
[ -f "${PACKAGE_NAME}" ] && rm "${PACKAGE_NAME}"

# Build the package
fpm -s dir -t deb -n ${PKG_NAME} -v ${VERSION} -a ${ARCHITECTURE} \
    --description "${DESCRIPTION}" \
    --prefix /opt/${PKG_NAME} \
    --depends python3-boto3 \
    --depends python3-requests \
    --after-install packaging/postinst.sh \
    --before-remove packaging/prerm.sh \
    --config-files \
    ./python/ \
    ./systemd/${PKG_NAME}.service \
    ./packaging/config_template=config
