#!/bin/sh
set -eu

envf=${PWD}/secret/heroku.env

userdir=${HOME}/uws/heroku
install -v -d -m 0750 ${userdir}

exec docker run -it --rm --name uws-heroku-devel \
	--hostname heroku-devel.uws.local \
	-u uws \
	--env-file "${envf}" \
	-v "${userdir}:/home/uws/download" \
	uws/heroku
