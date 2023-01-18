#!/bin/sh
set -eu

APP=${1:?'app name?'}

cd "${HOME}/download"

heroku config -s -a "${APP}" >"${APP}.env.new"
< "${APP}.env.new" sed 's#^#export #' >"${APP}.env"
rm -vf "${APP}.env.new"

exit 0
