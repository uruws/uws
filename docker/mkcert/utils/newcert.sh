#!/bin/sh
set -eu
umask 0027
exec mkcert -ecdsa $@
