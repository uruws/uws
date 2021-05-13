#!/bin/sh
set -eu
. ~/bin/env.export
uwskube delete -f ~/k8s/ca/deploy.yaml
exit 0
