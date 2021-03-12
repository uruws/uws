#!/bin/sh
set -eu
if ! test -s /home/uws/api/app.env; then
	echo "api/app.env: file not found" >&2
	exit 1
fi
. /home/uws/api/app.env
cd /home/uws/api/app
exec ./.meteor/heroku_build/bin/node .meteor/heroku_build/app/main.js
