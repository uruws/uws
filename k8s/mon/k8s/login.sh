#!/bin/sh
set -eu
exec uwskube exec deploy/k8s -i -t -n mon -- bash -il
