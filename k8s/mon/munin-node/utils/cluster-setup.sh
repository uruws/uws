#!/bin/sh
set -eu

install -v -m 0755 /srv/etc/munin-node/k8smon.sh /usr/local/bin/k8smon

enpl=/root/bin/plugin-enable.sh

${enpl} local k8smon nodes

exit 0
