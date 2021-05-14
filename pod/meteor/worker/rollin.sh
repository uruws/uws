#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
uwskube delete -n meteor-worker -f ${pod}/deploy.yaml --wait
exit 0
