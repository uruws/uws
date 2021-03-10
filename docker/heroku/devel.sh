#!/bin/sh
set -eu
HEROKU_API_KEY=${HEROKU_API_KEY:-''}
exec docker run -it --rm --name uws-heroku-devel \
	--hostname heroku-devel.uws.local -u uws \
	-e HEROKU_API_KEY=${HEROKU_API_KEY} \
	uws/heroku $@
