#!/bin/sh
set -eu

echo 'x - setup'

echo 'x - extract assets'
chmod -v 0750 /etc/cloud/cloud.cfg.d/99zzzuws_assets.sh
oldwd=${PWD}
cd /
/etc/cloud/cloud.cfg.d/99zzzuws_assets.sh -c
cd ${oldwd}

if test -d /uws/init; then
	echo 'x - run-parts /uws/init scripts'
	chmod -v 0755 /uws/init/* || true
	run-parts --report /uws/init
fi

exit 0
