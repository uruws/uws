#!/bin/sh
set -eu
envfn="/srv/uws/deploy/secret/cli/botija/${BOTIJA_ENV:-prod}/botija.env"
# shellcheck disable=SC1090
. "${envfn}"
exec /opt/uwscli/bin/python3 /srv/home/uwscli/lib/botija.py "$@"
