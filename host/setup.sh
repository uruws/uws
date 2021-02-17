#!/bin/sh
set -eu

echo 'i - setup'
umask 0027
oldwd=${PWD}

echo 'x - extract assets'
chmod -v 0750 /etc/cloud/cloud.cfg.d/99zzzuws_assets.sh
cd /
/etc/cloud/cloud.cfg.d/99zzzuws_assets.sh -c
cd ${oldwd}

echo 'i - run init scripts'
if test -d /uws/init; then
	echo 'x - run-parts /uws/init scripts'
	chmod -v 0755 /uws/init/*
	run-parts --verbose /uws/init
	rm -rfv /uws/init
fi
cd ${oldwd}

exit 0
