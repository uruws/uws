#!/bin/sh
set -eu
uwskube create secret generic acme-prod-account-key \
	--from-file=tls.key=${HOME}/secret/acme/accounts/acme-v02.prod
uwskube apply -f ~/k8s/acme/prod.yaml
exit 0
