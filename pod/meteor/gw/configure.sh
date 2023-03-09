#!/bin/sh

gateway_configure() (
	ns="${1}"
	cfgdir="${2}"

	nginx_conf=${HOME}/pod/meteor/gw/nginx.conf
	if test -s "${cfgdir}/nginx.conf"; then
		nginx_conf="${cfgdir}/nginx.conf"
	fi

	install -d -m 0750 "${cfgdir}"
	install -d -m 0750 "${cfgdir}/nginx"
	install -v -d -m 0750 "${cfgdir}/nginx/sites-enabled"

	echo "nginx conf: ${nginx_conf}"
	envsubst <"${nginx_conf}" >"${cfgdir}/nginx/sites-enabled/meteor-${ns}"

	install -v -d -m 0750 "${cfgdir}/nginx/service"
	envsubst <~/pod/meteor/gw/service/meteor.yaml >"${cfgdir}/nginx/service/meteor-${ns}.yaml"
)
