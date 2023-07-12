#!/bin/sh
set -eu

ABENCH_TAG=$(cat ./srv/ab/VERSION)

./host/ecr-login.sh us-east-1
./cluster/ecr-push.sh us-east-1 uws/ab-2305 "uws:ab-${ABENCH_TAG}"

if test -d /srv/www/ssl/htmlcov; then
	if test -d ./tmp/ab/htmlcov; then
		umask 0022
		cp -r ./tmp/ab/htmlcov /srv/www/ssl/htmlcov/ab
		echo '/srv/www/ssl/htmlcov/ab done!'
	fi
fi

exit 0
