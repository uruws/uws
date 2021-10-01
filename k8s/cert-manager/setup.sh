#!/bin/sh
set -eu
uwskube create namespace cert-manager
exec ~/k8s/cert-manager/install.sh
