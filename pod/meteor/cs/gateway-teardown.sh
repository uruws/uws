#!/bin/sh
set -eu
cat ~/pod/meteor/cs/gateway-${METEOR_CS_ENV}.yaml \
	~/pod/meteor/cs/gateway-common.yaml |
	envsubst | uwskube delete -f -
exit 0
