#!/bin/sh
set -eu
pod=/home/uws/pod/nlp
uwskube delete -f ${pod}/deploy.yaml
exit 0
