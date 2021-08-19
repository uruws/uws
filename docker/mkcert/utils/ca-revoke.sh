#!/bin/sh
set -eu
CRT=${1:?'cert(s)?'}
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
openssl ca -revoke "$@"
exit 0
