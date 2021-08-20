#!/bin/sh
set -eu
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
for fn in $(ls ${HOME}/ca/revoke/new/*.pem 2>/dev/null); do
	echo "ca revoke: ${fn}"
	openssl ca -revoke "${fn}"
done
exec ca-crl.sh
