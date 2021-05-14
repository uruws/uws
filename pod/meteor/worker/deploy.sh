#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
uwskube apply -n meteor-worker -f ${pod}/deploy.yaml
exit 0
