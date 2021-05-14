#!/bin/sh
set -eu
pod=/home/uws/pod/nlp
uwskube apply -f ${pod}/deploy.yaml
exit 0
