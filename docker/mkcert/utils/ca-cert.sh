#!/bin/sh
set -eu
DOMAIN=${1:?'cert domain?'}
umask 0027

fn=$(uuidgen.sh "${DOMAIN}")

mkcert -ecdsa -cert-file "${HOME}/ca/cert/${fn}.pem" \
	-key-file "${HOME}/ca/cert/${fn}-key.pem" "$@"

#~ export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
#~ openssl verify -verbose -CAfile "${HOME}/ca/rootCA.pem" "${HOME}/ca/cert/${fn}.pem"

chain_file="${HOME}/ca/cert/${fn}-chain.pem"
cat "${HOME}/ca/cert/${fn}-key.pem" >${chain_file}
cat "${HOME}/ca/cert/${fn}.pem" >>${chain_file}
cat "${HOME}/ca/rootCA.pem" >>${chain_file}

exit 0
