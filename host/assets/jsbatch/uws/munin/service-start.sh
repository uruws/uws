#!/bin/sh
set -eu
CA=/srv/uws/deploy/secret/ca/uws/smtps/211006
HOSTIP=$(/uws/docker-hostip.sh)
exec /usr/bin/docker run --rm -u root \
	--name uws-munin-service \
	--hostname munin.uws.local \
	--add-host docker.uws.local:${HOSTIP} \
	-v /srv/munin/var/lib:/var/lib/munin \
	-v /srv/munin/var/alert:/var/opt/munin-alert \
	-v /srv/munin/var/log:/var/log/munin \
	-v /srv/munin/cache/www:/var/cache/munin/www \
	-v /srv/etc/munin:/srv/etc/munin \
	-v ${CA}/client:/srv/etc/ca:ro \
	-e UWS_SMTPS='ops.uws.talkingpts.org' \
	-e UWS_SMTPS_CERT='/etc/opt/uws/ca/smtps.pem' \
	-e UWS_SMTPS_KEY='/etc/opt/uws/ca/smtps.key' \
	uws/munin
