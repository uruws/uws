#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
uwskube apply -f ${pod}/deploy.yaml
exit 0
