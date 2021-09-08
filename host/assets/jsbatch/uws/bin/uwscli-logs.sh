#!/bin/sh
set -eu

find ~/logs/ -type f -name '*-build-*.log' -mtime +2 -exec gzip -v9 {} \;

if test -s ~/logs/app-ctl.log; then
	dst=app-ctl-$(date '+%y%m%d').log
	mv -vf ~/logs/app-ctl.log ~/logs/${dst}
	gzip -v9 ~/logs/${dst}
fi

find ~/logs/ -type f -name '*.log.gz' -mtime +30 -exec rm -vf {} \;

exit 0
