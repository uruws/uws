#!/bin/sh

gateway_configure() (
	cfgdir="${1}"

	install -v -d -m 0750 "${cfgdir}"
	install -d -m 0750 "${cfgdir}/nginx"
	install -d -m 0750 "${cfgdir}/nginx/sites-enabled"

	envsubst <~/k8s/gateway/cluster.conf >"${cfgdir}/nginx/sites-enabled/cluster-gateway"
)
