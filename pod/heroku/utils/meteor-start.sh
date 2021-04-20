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
appenv=/run/meteor/app.env
echo "--- ${appenv}"
if ! test -s ${appenv}; then
	echo "${appenv}: file not found" >&2
	exit 1
fi
ls -lh ${appenv}
tail ${appenv}
echo "--- DEBUG end"
. ${appenv}
cd /home/uws/meteor/app
exec ./.meteor/heroku_build/bin/node ./.meteor/heroku_build/app/main.js
