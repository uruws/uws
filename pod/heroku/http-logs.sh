#!/bin/sh
set -eu
./pod/heroku/logs.sh -n ingress-nginx service/ingress-nginx-controller --prefix=false $@
exit 0
