#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/beta
uwskube apply -n meteor-beta -f ${pod}/deploy.yaml
exit 0
