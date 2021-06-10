#!/bin/sh
set -eu
ns=${1:?'namespace?'}
pod=/home/uws/pod/meteor/web
uwskube delete -n ${ns} -f ${pod}/deploy.yaml
exit 0
