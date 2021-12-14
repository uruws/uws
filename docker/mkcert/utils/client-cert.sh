#!/bin/sh
set -eu
umask 0027
exec mkcert -client -ecdsa -pkcs12 "$@"
