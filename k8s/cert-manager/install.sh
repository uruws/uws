#!/bin/sh
set -eu

helm repo add jetstack https://charts.jetstack.io
helm repo update

exec helm upgrade --install cert-manager jetstack/cert-manager \
	--namespace cert-manager \
	--version 1.7.1 \
	--set installCRDs=true
