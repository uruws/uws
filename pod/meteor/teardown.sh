#!/bin/sh
set -eu
uwskube delete configmap deploy-env -n meteor || true
uwskube delete namespace meteor
exit 0
