#!/bin/sh

meteor_backend_configure() (
	ns="${1}"
	replicas="${2}"
	echo "upstream meteor-${ns} {"
	echo '    random two least_conn;'
	for idx in $(seq 0 "${replicas}"); do
		echo "    server meteor${idx}-${ns}:3000;"
	done
	echo '}'
)

meteor_service_configure() (
	ns="${1}"
	replicas="${2}"
	for idx in $(seq 0 "${replicas}"); do
		echo '---'
		echo 'apiVersion: v1'
		echo 'kind: Service'
		echo 'metadata:'
		echo "  name: meteor${idx}-${ns}"
		echo 'spec:'
		echo '  type: ExternalName'
		echo "  externalName: meteor.${ns}.svc.cluster.local"
	done
)

gateway_configure() (
	ns="${1}"
	cfgdir="${2}"

	nginx_conf=${HOME}/pod/tapo/ngx/nginx.conf
	if test -s "${cfgdir}/nginx.conf"; then
		nginx_conf="${cfgdir}/nginx.conf"
	fi

	install -d -m 0750 "${cfgdir}"
	install -d -m 0750 "${cfgdir}/nginx"
	install -v -d -m 0750 "${cfgdir}/nginx/sites-enabled"

	echo "nginx conf: ${nginx_conf}"

	meteor_backend_configure "${ns}" "${NGINX_REPLICAS}" \
		>"${cfgdir}/nginx/sites-enabled/meteor-${ns}"

	if test -s "${cfgdir}/meteor-backend-configure.sh"; then
		/bin/sh "${cfgdir}/meteor-backend-configure.sh" \
			>>"${cfgdir}/nginx/sites-enabled/meteor-${ns}"
	fi

	<"${nginx_conf}" envsubst '${METEOR_NAMESPACE}' |
		envsubst '${METEOR_HOST}' |
		envsubst '${METEOR_TLS}' >>"${cfgdir}/nginx/sites-enabled/meteor-${ns}"

	install -v -d -m 0750 "${cfgdir}/nginx/service"
	meteor_service_configure "${ns}" "${NGINX_REPLICAS}" \
		>"${cfgdir}/nginx/service/meteor-${ns}.yaml"
)
