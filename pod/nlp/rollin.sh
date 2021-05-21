#!/bin/sh
set -eu
pod=/home/uws/pod/nlp
uwskube delete -f ${pod}/api/deploy.yaml
uwskube delete -f ${pod}/ner/deploy.yaml
uwskube delete -f ${pod}/sentiment/deploy.yaml
exit 0
