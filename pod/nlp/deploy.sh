#!/bin/sh
set -eu
pod=/home/uws/pod/nlp
uwskube apply -f ${pod}/api/deploy.yaml
uwskube apply -f ${pod}/ner/deploy.yaml
uwskube apply -f ${pod}/sentiment/deploy.yaml
exit 0
