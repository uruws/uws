#!/bin/sh
set -eu
uwskube delete secret -n worker meteor-app-env
uwskube delete namespace worker
exit 0
