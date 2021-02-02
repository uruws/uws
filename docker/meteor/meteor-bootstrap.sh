#!/bin/sh
set -eu

TARGZ_URL='https://static-meteor.netdna-ssl.com/packages-bootstrap/1.10.2/meteor-bootstrap-os.linux.x86_64.tar.gz'
TARGZ='meteor-bootstrap.tgz'

wget -O ${TARGZ} ${TARGZ_URL}

# FIXME

exit 0
