#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get -q install -yy --purge --no-install-recommends "$@"
exit 0
