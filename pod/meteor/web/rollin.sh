#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/web
uwskube delete secret -n meteor-web meteor-web-env
uwskube delete -n meteor-web -f ${pod}/deploy.yaml
exit 0
