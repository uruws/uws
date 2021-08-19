#!/bin/sh
set -eu
DOMAIN=${1:-'cert domain?'}
umask 0027
exec mkcert -ecdsa -cert-file "${HOME}/ca/cert/${DOMAIN}.pem" \
	-key-file "${HOME}/ca/cert/${DOMAIN}-key.pem" "$@"
