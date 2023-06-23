#!/bin/sh
set -eu

CROND=/srv/uws/deploy/secret/eks/files/munin/cron.d
CONFD=/srv/uws/deploy/secret/eks/files/munin/conf
MAILX=/srv/uws/deploy/secret/eks/files/mailx/aws.ses

HOSTIP=$(/uws/docker-hostip.sh)

exec /usr/bin/docker run --rm -u root \
	--name uws-munin-service \
	--hostname munin.uws.local \
	--add-host "docker.uws.local:${HOSTIP}" \
	-v /srv/munin/var/lib:/var/lib/munin \
	-v /srv/munin/var/alert:/var/opt/munin-alert \
	-v /srv/munin/var/log:/var/log/munin \
	-v /srv/munin/cache/www:/var/cache/munin/www \
	-v /srv/etc/munin:/srv/etc/munin \
	-v "${CROND}:/srv/etc/cron.d:ro" \
	-v "${CONFD}:/etc/uws/conf:ro" \
	-v "${MAILX}:/srv/mailx/etc:ro" \
	uws/munin-2305
