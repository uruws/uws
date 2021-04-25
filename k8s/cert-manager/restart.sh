#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube rollout -n cert-manager restart deployment
