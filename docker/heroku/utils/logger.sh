#!/bin/sh
set -eu
env=${1:?'app env?'}
. /home/uws/auth/heroku.env
exec heroku logs -t -a "tapo${env}" -s app
