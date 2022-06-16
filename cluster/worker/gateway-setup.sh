#!/bin/sh
set -eu
exec uwskube apply -f ~/cluster/gateway.yaml
