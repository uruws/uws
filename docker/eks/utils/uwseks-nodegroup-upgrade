#!/bin/sh
set -eu
exec uwseks upgrade nodegroup --wait=false --color=false \
	--name=main --kubernetes-version=${K8S_VERSION}
