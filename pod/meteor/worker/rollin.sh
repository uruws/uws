#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
meteor-worker delete secret -n meteor-web meteor-web-env
meteor-worker delete -n meteor-web -f ${pod}/deploy.yaml
exit 0
