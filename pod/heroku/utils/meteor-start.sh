#!/bin/sh
set -eu
echo "--- DEBUG start"
echo "--- user"
id -a
echo "--- env"
env | sort
echo "--- meteor"
ls -lh /home/uws/meteor
ls -lh /home/uws/meteor/app
echo "--- mount"
(mount | grep /home/uws/meteor/app) || true
echo "--- app.env"
if ! test -s /run/app.env; then
	echo "/run/app.env: file not found" >&2
	exit 1
fi
ls -lh /run/app.env
tail /run/app.env
echo "--- DEBUG end"
. /run/app.env
cd /home/uws/meteor/app
exec ./.meteor/heroku_build/bin/node ./.meteor/heroku_build/app/main.js
