#!/bin/sh
set -eu
exec docker run --rm \
	--name uws-kali \
	--hostname kali.uws.local \
	-v ${PWD}/secret/kali:/root/etc \
	--tmpfs /tmp:rw,mode=1777 \
	-p 127.0.0.1:3327:3327 \
	uws/kali /usr/local/bin/kali-start.sh
