#!/bin/sh
set -eu
CA=smtps/211006
exec docker run --rm --name herokud \
	--hostname herokud.uws.local \
	--read-only \
	-v "/srv/uws/deploy/secret/ca/uws/${CA}:/srv/etc/ca:ro" \
	--tmpfs /home/uws/.cache/heroku \
	--tmpfs /run \
	--tmpfs /tmp \
	uws/herokud
