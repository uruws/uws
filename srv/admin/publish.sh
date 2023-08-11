#!/bin/sh
set -eu

ADMIN_TAG=$(cat ./srv/admin/VERSION)

./host/ecr-login.sh us-east-1
./cluster/ecr-push.sh us-east-1 uws/admin-2305 "uws:admin-${ADMIN_TAG}"

if test -d /srv/www/ssl/htmlcov; then
	if test -d ./tmp/admin/htmlcov; then
		umask 0022
		cp -r ./tmp/admin/htmlcov /srv/www/ssl/htmlcov/admin
		echo '/srv/www/ssl/htmlcov/admin done!'
	fi
fi

#docker tag uws/admin-2305 "uws/admin-${ADMIN_TAG}"

exit 0
