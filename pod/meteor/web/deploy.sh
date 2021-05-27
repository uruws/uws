#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/web
uwskube apply -n meteor-web -f ${pod}/deploy.yaml
exit 0
