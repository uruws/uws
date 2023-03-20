#!/bin/sh
set -eu

find ~/logs/ -type f -name '*-build-*.log' -mtime +2 -exec gzip -9 {} \;
find ~/logs/ -type f -name 'deploy-*.log' -mtime +2 -exec gzip -9 {} \;

if test -s ~/logs/app-ctl.log; then
	# run on sundays only
	if test 'X0' = "X$(date '+%w')"; then
		dst=app-ctl-$(date '+%y%m%d').log
		mv -f ~/logs/app-ctl.log "${HOME}/logs/${dst}"
		gzip -9 "${HOME}/logs/${dst}"
	fi
fi

if test -s ~/logs/uwsq.log; then
	# run on sundays only
	if test 'X0' = "X$(date '+%w')"; then
		dst=uwsq-$(date '+%y%m%d').log
		mv -f ~/logs/uwsq.log "${HOME}/logs/${dst}"
		gzip -9 "${HOME}/logs/${dst}"
	fi
fi

find ~/logs/ -type f -name '*.log.gz' -mtime +400 -exec rm -f {} \;

exit 0
