#!/bin/sh
set -eu
exec docker run -it --rm --name uws-golang-docs \
	--hostname go-docs.uws.local -u uws \
	-v ${PWD}/go:/go/src/uws \
	-p 127.0.0.1:6060:6060 \
	--entrypoint /usr/local/bin/godoc.sh \
	uws/golang-2305
