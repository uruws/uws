#!/bin/sh
set -eu
exec uwskube apply -f ~/cluster/worker-gateway.yaml
