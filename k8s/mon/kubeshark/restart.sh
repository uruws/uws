#!/bin/sh
set -eu
exec uwskube rollout restart deployment kubeshark -n mon
