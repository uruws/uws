#!/bin/sh
set -eu
HEROKU_API_KEY=${HEROKU_API_KEY:-''}
srvdir=/srv/heroku/download
mkdir -vp ${srvdir}
exec docker run -it --rm --name uws-heroku-cmd \
	--hostname heroku-cmd.uws.local -u uws \
	-e HEROKU_API_KEY=${HEROKU_API_KEY} \
	-v ${srvdir}:/home/uws/download \
	uws/heroku $@
