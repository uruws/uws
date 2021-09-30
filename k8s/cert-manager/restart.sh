#!/bin/sh
set -eu
exec uwskube rollout -n cert-manager restart deployment
