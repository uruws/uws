#!/bin/sh
set -eu
uwskube delete secret -n meteor-beta meteor-beta-env || true
uwskube delete namespace meteor-beta
exit 0
