#!/bin/sh
set -eu
DOMAIN=${1:-'cert domain?'}
umask 0027
exec mkcert -ecdsa -cert-file "${HOME}/ca/crt/${DOMAIN}.pem" \
	-key-file "${HOME}/ca/key/${DOMAIN}.pem" "$@"
