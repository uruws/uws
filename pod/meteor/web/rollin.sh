#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/web
uwskube delete -f ${pod}/deploy.yaml
exit 0
