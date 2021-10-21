#!/bin/sh
set -eu
exec docker run --rm -it --read-only \
	--name uws-kali \
	--hostname kali.uws.local \
	--tmpfs /tmp:rw,mode=1777 \
	uws/kali
