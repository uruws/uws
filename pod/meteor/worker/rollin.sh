#!/bin/sh
set -eu
pod=/home/uws/pod/meteor/worker
uwskube delete -f ${pod}/deploy.yaml
exit 0
