#!/bin/sh

haproxy_ingress_configure() (
	set -eu

	action=${1:?'haproxy configure action?'}
	envfn=${2:?'haproxy env configure file?'}
	ingfn=${3:?'haproxy ingress configure file?'}

	ingcfg="${HOME}/k8s/haproxy/ingress/configure.yaml"

	export HPX_NAME=haproxy-ingress
	export HPX_NAMESPACE=default
	export HPX_HOSTNAME="${CLUSTER_HOST}.uws"
	export HPX_TLS=uwsgd-tls

	# shellcheck disable=SC1090
	. "${envfn}"

	<"${ingfn}" envsubst '${HPX_NAME}'      |
		        envsubst '${HPX_NAMESPACE}' |
		        envsubst '${HPX_HOSTNAME}'  |
		        envsubst '${HPX_TLS}'       |
		uwskube "${action}" -n "${HPX_NAMESPACE}" -f -

	<"${ingcfg}" envsubst '${HPX_NAME}'      |
			     envsubst '${HPX_NAMESPACE}' |
		uwskube "${action}" -n "${HPX_NAMESPACE}" -f -
)
