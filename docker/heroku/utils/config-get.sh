#!/bin/bash
set -eu

APP=${1:?'app name?'}

cd "${HOME}/download"

heroku config -s -a "${APP}" >"${APP}.env.new"

grep -vE '^METEOR_SETTINGS=' "${APP}.env.new" |
	sed 's#^#export #' >"${APP}.env"

grep -E '^METEOR_SETTINGS=' "${APP}.env.new" |
	sed 's#^#export #' >"${APP}-settings.env"

rm -vf "${APP}.env.new"

# shellcheck disable=SC1090
source "${APP}-settings.env"
rm -vf "${APP}-settings.env"

echo -ne "${METEOR_SETTINGS}" >"${APP}-settings.json"

exit 0
