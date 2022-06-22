#!/bin/sh
set -eu
~/ca/godaddyCerts/teardown.sh
exec uwskube delete -f ~/cluster/gateway.yaml
