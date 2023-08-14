#!/bin/sh
set -eu
admin_env=${1:?'admin env?'}
exec /usr/bin/docker kill "uwsadm-${admin_env}"
