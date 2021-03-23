#!/bin/sh
set -eu
export UWS_STATSDIR=/srv/uwsbot/stats/testing
exec /uws/bin/uwsbot -env testing -name api
