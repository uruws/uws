#!/bin/sh
set -u
helm uninstall --namespace cert-manager cert-manager
uwskube delete namespace cert-manager
exit 0
