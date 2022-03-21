#!/bin/sh
set -eu
exec envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml |
	uwskube apply -f -
