#!/bin/sh
set -eu
env=${1:?'app env?'}
. /home/uws/auth/heroku.env
export UWS_LOG=quiet
stdir=/home/uws/stats
exec heroku logs -a "tapo${env}" -s app -d web | grep -F ': PARSER_' |
	sort -k1,1 -u | api-logs -statedir ${stdir} -statsdir ${stdir} -filter -
