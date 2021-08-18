#!/bin/sh
set -eu
EMAIL=${1:-'user email?'}
umask 0027
exec mkcert -client -ecdsa -pkcs12 --p12-file "${HOME}/ca/client/${EMAIL}.p12" "$@"
