#!/bin/sh
set -eu
uwskube create namespace ctl
exec ~/k8s/ctl/deploy.sh
