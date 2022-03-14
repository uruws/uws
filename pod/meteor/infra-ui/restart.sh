#!/bin/sh
set -eu
exec uwskube rollout restart deployment -n infra-ui
