#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/beta
uwskube delete secret -n meteor-beta meteor-beta-env
uwskube delete -n meteor-beta -f ${pod}/deploy.yaml
exit 0
