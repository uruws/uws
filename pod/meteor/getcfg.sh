#!/bin/sh
set -eu
uwskube get configmap deploy-env -n meteor -o jsonpath='{.data.deploy-env}'
exit 0
