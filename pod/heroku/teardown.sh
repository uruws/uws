#!/bin/sh
set -eu
pod=/home/uws/pod/heroku
uwskube delete -f ${pod}/deploy.yaml --wait
uwskube delete secret heroku-meteor-app-env
exit 0
