#!/bin/sh
set -eu
VERSION='210811'
make munin-deploy MON_TAG=${VERSION}
exit 0
