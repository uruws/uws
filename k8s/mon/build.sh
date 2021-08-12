#!/bin/sh
set -eu
VERSION="$(cat ./k8s/mon/VERSION)"
make munin-deploy MON_TAG=${VERSION}
exit 0
