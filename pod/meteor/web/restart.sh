#!/bin/sh
set -eu
uwskube rollout restart deployment -n web
exit 0
