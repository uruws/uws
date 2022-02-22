#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/211006
exec docker run -it --rm --name uws-crond \
	--hostname crond.uws.local \
	-v ${CA}/client:/srv/etc/ca:ro \
	uws/crond
