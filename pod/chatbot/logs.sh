#!/bin/sh
set -eu
uwscb_ns="cb${UWSCB_ENV}"
exec ~/pod/lib/logs.py -n "${uwscb_ns}" \
	-l 'app.kubernetes.io/name=webapp' \
	"$@"
