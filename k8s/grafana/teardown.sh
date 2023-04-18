#!/bin/sh
set -u
~/k8s/grafana/uninstall.sh
exec uwskube delete namespace grfn
