#!/bin/sh
set -eu
./pod/heroku/logs.sh -n ingress-nginx service/ingress-nginx-controller --prefix=false $@ |
	fgrep heroku-meteor-service
exit 0
