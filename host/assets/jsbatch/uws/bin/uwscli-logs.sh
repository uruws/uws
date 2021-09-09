#!/bin/sh
set -eu

find ~/logs/ -type f -name '*-build-*.log' -mtime +2 -exec gzip -9 {} \;

if test -s ~/logs/app-ctl.log; then
	# run on sundays only
	if test 'X0' = "X$(date '+%w')"; then
		dst=app-ctl-$(date '+%y%m%d').log
		mv -f ~/logs/app-ctl.log ~/logs/${dst}
		gzip -9 ~/logs/${dst}
	fi
fi

find ~/logs/ -type f -name '*.log.gz' -mtime +30 -exec rm -f {} \;

exit 0
