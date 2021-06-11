#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/web
uwskube apply -f ${pod}/deploy.yaml
exit 0
