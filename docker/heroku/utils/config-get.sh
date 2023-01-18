#!/bin/bash
set -eu

APP=${1:?'app name?'}

cd "${HOME}/download"

heroku config -s -a "${APP}" >"${APP}.env.new"

grep -vE '^METEOR_SETTINGS=' "${APP}.env.new" |
	sed 's#^#export #' >"${APP}.env"

grep -vE '^METEOR_SETTINGS=' "${APP}.env.new" >"${APP}-settings.env"

rm -vf "${APP}.env.new"

source "${APP}-settings.env"
rm -vf "${APP}-settings.env"

echo -ne "${METEOR_SETTINGS}" >"${APP}-settings.json"

exit 0
