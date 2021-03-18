#!/bin/sh
set -eu
env=${1:?'app env?'}
. /home/uws/auth/heroku.env
exec heroku logs -a "tapo${env}" -s app | grep -F ': PARSER_'
