#!/bin/sh
set -u
cluster="$(basename "$(dirname "$0")")"
echo "*** admin: ${cluster}"
exec ./eks/admin.sh "${cluster}"
