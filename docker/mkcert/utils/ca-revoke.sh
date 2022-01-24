#!/bin/sh
set -eu
umask 0027
export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
if test -d ${HOME}/ca/revoke/new; then
	for fn in ${HOME}/ca/revoke/new/*.pem; do
		echo "ca revoke: ${fn}"
		openssl ca -revoke "${fn}"
		mv -f "${fn}" "${HOME}/ca/revoke/$(basename "${fn}")"
	done
fi
exec ca-crl.sh
