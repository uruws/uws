#!/bin/sh
set -eu
DOMAIN=${1:-'cert domain?'}
umask 0027

fn=$(uuidgen --sha1 --namespace '@dns' --name "${DOMAIN}")

mkcert -ecdsa -cert-file "${HOME}/ca/cert/${fn}.pem" \
	-key-file "${HOME}/ca/cert/${fn}-key.pem" "$@"

chain_file="${HOME}/ca/cert/${fn}-chain.pem"
cat "${HOME}/ca/cert/${fn}.pem" >${chain_file}
cat "${HOME}/ca/rootCA.pem" >>${chain_file}

exit 0
