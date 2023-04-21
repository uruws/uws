haproxy_configure() (
	set -eu

	dstfn=${1:?'haproxy dest values file?'}
	envfn=${2:?'haproxy env configure file?'}

	srcfn="${HOME}/k8s/haproxy/values.yaml"
	ingclfn="${HOME}/k8s/haproxy/ingress-class.yaml"

	export HPX_NAMESPACE=default
	export HPX_DEFAULT_BACKEND=defaulthpx/haproxy-ingress-default-backend
	export HPX_ENABLE_DEFAULT_BACKEND=false
	export HPX_ENABLE_AUTOSCALING=true
	export HPX_REPLICAS=3

	# shellcheck disable=SC1090
	. "${envfn}"

	envsubst '${HPX_NAMESPACE}' <"${srcfn}"      |
		envsubst '${HPX_DEFAULT_BACKEND}'        |
		envsubst '${HPX_ENABLE_DEFAULT_BACKEND}' |
		envsubst '${HPX_ENABLE_AUTOSCALING}'     |
		envsubst '${HPX_REPLICAS}' >"${dstfn}"

	envsubst '${HPX_NAMESPACE}' <"${ingclfn}" |
		uwskube apply -n "${HPX_NAMESPACE}" -f -
)