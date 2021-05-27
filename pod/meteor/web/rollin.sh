#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/web
uwskube delete -n meteor-web -f ${pod}/deploy.yaml
exit 0
