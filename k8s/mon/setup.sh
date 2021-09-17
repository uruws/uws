#!/bin/sh
set -eu
uwskube create namespace mon
exec ~/k8s/mon/deploy.sh
