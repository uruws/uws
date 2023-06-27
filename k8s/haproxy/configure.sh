#!/bin/sh

haproxy_configure() (
	set -eu

	dstfn=${1:?'haproxy configure dest file?'}
	prof=${2:?'haproxy configure profile?'}

	srcfn="${HOME}/k8s/haproxy/values.yaml"
	ingclfn="${HOME}/k8s/haproxy/ingress/class.yaml"

	envfn="${HOME}/${prof}/haproxy.env"

	export HPX_NAME=defhpx
	export HPX_NAMESPACE=default
	export HPX_DEFAULT_BACKEND=default/defhpx-haproxy-ingress-default-backend
	export HPX_ENABLE_DEFAULT_BACKEND=false
	export HPX_ENABLE_AUTOSCALING=true
	export HPX_REPLICAS=3

	# shellcheck disable=SC1090
	. "${envfn}"

	envsubst '${HPX_NAME}' <"${srcfn}"           |
		envsubst '${HPX_NAMESPACE}'              |
		envsubst '${HPX_DEFAULT_BACKEND}'        |
		envsubst '${HPX_ENABLE_DEFAULT_BACKEND}' |
		envsubst '${HPX_ENABLE_AUTOSCALING}'     |
		envsubst '${HPX_REPLICAS}' >"${dstfn}"

	envsubst '${HPX_NAME}' <"${ingclfn}" |
		uwskube apply -n "${HPX_NAMESPACE}" -f -
)
