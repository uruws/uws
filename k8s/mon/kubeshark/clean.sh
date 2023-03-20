#!/bin/sh
set -eu
exec /usr/local/bin/kubeshark-start.sh "${UWS_CLUSTER}" clean
