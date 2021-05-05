#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
uwskube delete secret -n meteor-worker meteor-worker-env
uwskube delete -n meteor-worker -f ${pod}/deploy.yaml
exit 0
