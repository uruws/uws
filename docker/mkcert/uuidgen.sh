#!/bin/sh
set -eu
exec docker run --rm --network none --name uws-mkcert-uuidgen \
	-u uws uws/mkcert-2305 uuidgen.sh "$@"
