#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube rollout -n ingress-nginx restart deployment
