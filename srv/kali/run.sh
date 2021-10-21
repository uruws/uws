#!/bin/sh
set -eu
exec docker run --rm -it --read-only \
	--name uws-kali \
	--hostname kali.uws.local \
	--tmpfs /tmp:rw,mode=1777 \
	-p 127.0.0.1:3327:8081 \
	uws/kali /usr/local/bin/kali-start.sh
