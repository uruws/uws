#!/bin/sh
set -eu
DOMAIN=${1:-'cert domain?'}
umask 0027

mkcert -ecdsa -cert-file "${HOME}/ca/cert/${DOMAIN}.pem" \
	-key-file "${HOME}/ca/cert/${DOMAIN}-key.pem" "$@"

chain_file="${HOME}/ca/cert/${DOMAIN}-chain.pem"
cat "${HOME}/ca/cert/${DOMAIN}.pem" >${chain_file}
cat "${HOME}/ca/rootCA.pem" >>${chain_file}

exit 0
