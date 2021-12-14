#!/bin/sh
set -eu
HEROKU_API_KEY=${HEROKU_API_KEY:-''}
userdir=${HOME}/uws/heroku
mkdir -vp ${userdir}
exec docker run -it --rm --name uws-heroku-devel \
	--hostname heroku-devel.uws.local -u uws \
	-e HEROKU_API_KEY=${HEROKU_API_KEY} \
	-v ${userdir}:/home/uws/download \
	uws/heroku "$@"
