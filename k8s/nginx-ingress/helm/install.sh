#!/bin/sh
set -eu

profile=${1:?'profile?'}

helm repo add nginx-stable https://helm.nginx.com/stable
helm repo update --fail-on-repo-update-fail

exec helm install \
	--values "./k8s/nginx-ingress/profile/${profile}.yaml" \
	--create-namespace --namespace "ingress-${profile}" \
	--wait --wait-for-jobs --timeout 5m0s \
	"${profile}" nginx-stable/nginx-ingress
