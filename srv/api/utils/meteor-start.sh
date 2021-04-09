#!/bin/sh
set -eu
echo "--- DEBUG"
echo "--- env"
env | sort
echo "--- meteor"
ls -lh /home/uws/meteor
ls -lh /home/uws/meteor/app
echo "--- mount"
(mount | grep /home/uws/meteor/app) || true
echo "--- DEBUG"
set -x
if ! test -s /home/uws/meteor/app.env; then
	echo "api/app.env: file not found" >&2
	exit 1
fi
. /home/uws/meteor/app.env
cd /home/uws/meteor/app
exec ./.meteor/heroku_build/bin/node .meteor/heroku_build/app/main.js
