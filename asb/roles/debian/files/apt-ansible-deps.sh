#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
exec apt-get install --no-install-recommends -yy -q python3 python3-apt python-apt-common
