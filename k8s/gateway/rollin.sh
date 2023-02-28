#!/bin/sh
set -eu

# meteor-vanilla
if test "X${METEOR_VANILLA_HOST:-NONE}" != 'XNONE'; then
	uwskube delete -f "${HOME}/pod/meteor/vanilla/gateway-service.yaml"
fi

exec ~/k8s/nginx/rollin.sh default k8s/gateway
