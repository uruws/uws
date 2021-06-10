#!/bin/sh
set -eu
ns=${1:?'namespace?'}
pod=/home/uws/pod/meteor/web
uwskube apply -n ${ns} -f ${pod}/deploy.yaml
exit 0
