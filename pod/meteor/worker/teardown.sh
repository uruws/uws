#!/bin/sh
set -eu
uwskube delete secret -n meteor-worker meteor-worker-env
uwskube delete namespace meteor-worker
exit 0
