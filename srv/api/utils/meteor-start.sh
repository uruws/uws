#!/bin/sh
set -eu
if ! test -s /home/uws/meteor/app.env; then
	echo "api/app.env: file not found" >&2
	exit 1
fi
. /home/uws/meteor/app.env
cd /home/uws/meteor/app
exec ./.meteor/heroku_build/bin/node .meteor/heroku_build/app/main.js
