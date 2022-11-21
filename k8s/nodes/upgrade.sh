#!/bin/sh
set -eu
exec ~/bin/uwseks upgrade nodegroup --wait=false --color=false \
	--name=main --kubernetes-version=${K8S_VERSION}
