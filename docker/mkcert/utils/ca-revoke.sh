#!/bin/sh
set -eu
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
for fn in $(ls ${HOME}/ca/revoke/*.pem); do
	echo "ca revoke: ${fn}"
	openssl ca -revoke "${fn}"
done
exec ca-crl.sh
