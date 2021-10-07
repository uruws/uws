#!/bin/sh
set -eu
CA=/srv/uws/deploy/secret/ca/uws/smtps/211006
HOSTIP=$(/uws/docker-hostip.sh)
exec /usr/bin/docker run --rm -u root \
	--name uws-munin-service \
	--hostname munin.uws.local \
	--add-host docker.uws.local:${HOSTIP} \
	-v ${CA}/client:/etc/opt/uws/ca:ro \
	-v /srv/munin/var/lib:/var/lib/munin \
	-v /srv/munin/var/alert:/var/opt/munin-alert \
	-v /srv/munin/var/log:/var/log/munin \
	-v /srv/munin/cache/www:/var/cache/munin/www \
	-v /srv/etc/munin:/srv/etc/munin \
	-e UWS_SMTPS='ops.uws.talkingpts.org' \
	-e UWS_SMTPS_CERT='/etc/opt/uws/ca/08082dca-8d77-5c81-9a44-94642089b3b1.pem' \
	-e UWS_SMTPS_KEY='/etc/opt/uws/ca/08082dca-8d77-5c81-9a44-94642089b3b1.key' \
	uws/munin
