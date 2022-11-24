#!/bin/sh
set -eu
profile=${1:?'profile?'}
uwskube get all -n "ingress-${profile}"
exit 0
