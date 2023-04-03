#!/bin/sh

gateway_configure() (
	cfgdir="${1}"

	nginx_conf=${HOME}/k8s/mon/kubeshark/gw/nginx.conf

	install -d -m 0750 "${cfgdir}"
	install -d -m 0750 "${cfgdir}/nginx"
	install -v -d -m 0750 "${cfgdir}/nginx/sites-enabled"

	<"${nginx_conf}" envsubst '${UWS_CLUSTER}' >"${cfgdir}/nginx/sites-enabled/meteor-${ns}"

	install -v -d -m 0750 "${cfgdir}/nginx/service"
	envsubst <~/k8s/mon/kubeshark/gw/service/kubeshark.yaml >"${cfgdir}/nginx/service/kubeshark.yaml"
)
