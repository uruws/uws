#!/bin/sh
set -eu
exec uwskube rollout -n ingress-nginx restart deployment
