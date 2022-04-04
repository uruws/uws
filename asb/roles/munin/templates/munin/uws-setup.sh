#!/bin/sh
# {{ ansible_managed | comment }}
set -eu

srcd=/usr/share/doc/munin/examples/nginx
sysd=/etc/systemd/system
install='install -v -m 0644 -o root -g root -C'

${install} ${srcd}/munin-* ${sysd}/

if ! systemctl is-enabled munin-graph.socket; then
	systemctl daemon-reload
	systemctl enable munin-graph.socket
	systemctl enable munin-html.socket
	systemctl start munin-graph.socket
	systemctl start munin-html.socket
fi

exit 0
