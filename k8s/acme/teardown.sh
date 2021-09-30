#!/bin/sh
set -eu
uwskube delete secret acme-prod-account-key
uwskube delete -f ~/k8s/acme/prod.yaml
exit 0
