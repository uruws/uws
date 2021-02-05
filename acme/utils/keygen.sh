#!/bin/sh
set -eu

umask 0027
mkdir -vp /srv/acme/key
umask 0077

NAME=${1:-'account'}
SIZE=${2:-'4096'}

FN=/srv/acme/key/${NAME}.key
if test -s ${FN}; then
	echo "${FN}: file already exists, aborting!" >&2
	exit 1
fi

openssl genrsa ${SIZE} >${FN}
echo "${FN}: done!"

exit 0
