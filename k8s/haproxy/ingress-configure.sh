haproxy_ingress_configure() (
	set -eu

	action=${1:?'haproxy configure action?'}
	envfn=${2:?'haproxy env configure file?'}
	ingfn=${3:?'haproxy ingress configure file?'}

	ingcfg="${HOME}/k8s/haproxy/ingress-config.yaml"

	export HPX_NAMESPACE=default
	export HPX_HOSTNAME="${CLUSTER_HOST}.uws"

	# shellcheck disable=SC1090
	. "${envfn}"

	<"${ingfn}" envsubst '${HPX_NAMESPACE}' |
		        envsubst '${HPX_HOSTNAME}'  |
		uwskube "${action}" -n "${HPX_NAMESPACE}" -f -

	<"${ingcfg}" envsubst '${HPX_NAMESPACE}' |
		uwskube "${action}" -n "${HPX_NAMESPACE}" -f -
)
