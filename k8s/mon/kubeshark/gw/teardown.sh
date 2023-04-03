#!/bin/sh
set -u
~/k8s/nginx/teardown.sh ksgw
exec uwskube delete namespace ksgw
