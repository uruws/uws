#!/bin/sh
set -eu
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
openssl ca -gencrl -out "${HOME}/ca/rootCA-crl.pem"
echo  "${HOME}/ca/rootCA-crl.pem updated!"
exit 0
