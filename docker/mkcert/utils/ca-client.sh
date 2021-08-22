#!/bin/sh
set -eu
EMAIL=${1:?'user email?'}
umask 0027

fn=$(uuidgen.sh "${EMAIL}")
p12fn="${HOME}/ca/client/${fn}.p12"

mkcert -client -ecdsa -pkcs12 --p12-file "${p12fn}" "$@"

exec ca-p12.sh "${fn}"
