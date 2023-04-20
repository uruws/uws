haproxy_ingress_configure() (
	set -eu

	dstfn=${1:?'haproxy dest ingress file?'}
	envfn=${2:?'haproxy env configure file?'}
	ingfn=${3:?'haproxy ingress configure file?'}

	export HPX_NAMESPACE=default
	export HPX_HOSTNAME="${UWS_CLUSTER}.uws"

	# shellcheck disable=SC1090
	. "${envfn}"

	envsubst '${HPX_NAMESPACE}' <"${ingfn}" |
		envsubst '${HPX_HOSTNAME}' >"${dstfn}"
)
