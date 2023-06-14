#!/bin/sh
set -eu
version=$(cat ${HOME}/pod/chatbot/VERSION)
uwscb_ns=cb${UWSCB_ENV}

APP_DEPLOY=$(date '+%y%m%d.%H%M%S')
export APP_DEPLOY

exec ~/pod/lib/deploy.sh "${uwscb_ns}" chatbot "${version}"
