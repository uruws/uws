#!/bin/sh
set -eu
uwskube create namespace grfn
exec ~/k8s/grafana/install.sh
