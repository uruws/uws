#!/bin/sh
set -eu
helm upgrade --install cert-manager jetstack/cert-manager \
	--repo https://charts.jetstack.io \
	--namespace cert-manager \
	--create-namespace \
	--set installCRDs=true
exit 0
