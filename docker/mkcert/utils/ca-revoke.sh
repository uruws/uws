#!/bin/sh
set -eu
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
for fn in ${HOME}/ca/revoke/new/*.pem; do
	echo "ca revoke: ${fn}"
	openssl ca -revoke "${fn}"
	mv -f "${fn}" "${HOME}/ca/revoke/$(basename "${fn}")"
done
exec ca-crl.sh
