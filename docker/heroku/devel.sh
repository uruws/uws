#!/bin/sh
exec docker run -it --rm --name uws-heroku-devel \
	--hostname heroku-devel.uws.local -u uws \
	uws/heroku $@
