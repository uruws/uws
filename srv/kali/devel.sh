#!/bin/sh
set -eu
exec docker run --rm -it \
	--name uws-kali-devel \
	--hostname kali-devel.uws.local \
	--tmpfs /tmp:rw,mode=1777 \
	-p 127.0.0.1:3327:3327 \
	uws/kali
