#!/bin/sh

gateway_configure() (
	cfgdir="${1}"

	install -v -d -m 0750 "${cfgdir}"
	install -d -m 0750 "${cfgdir}/nginx"
	install -d -m 0750 "${cfgdir}/nginx/sites-enabled"

	envsubst <~/k8s/gateway/cluster.conf >"${cfgdir}/nginx/sites-enabled/cluster-gateway"

	install -d -m 0750 "${cfgdir}/nginx/service"
	install -m 0640 -t "${cfgdir}/nginx/service" ~/k8s/gateway/service/*.yaml
)
