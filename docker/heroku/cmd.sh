#!/bin/sh
set -eu

envf=${PWD}/secret/heroku.env

srvdir=/srv/heroku/download
install -v -d -m 0750 ${srvdir}

exec docker run --rm --name uws-heroku-cmd \
	--hostname heroku-cmd.uws.local \
	-u uws \
	--env-file "${envf}" \
	-v "${srvdir}:/home/uws/download" \
	uws/heroku "$@"
