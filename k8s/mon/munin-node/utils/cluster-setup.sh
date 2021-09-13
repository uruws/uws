#!/bin/sh
set -eu

python3 -m compileall /srv/munin/plugins/*.py

install -v -m 0755 /srv/munin/plugins/k8smon.sh /usr/local/bin/k8smon
install -v -m 0755 /srv/munin/plugins/nginx.py /usr/local/bin/nginx

enpl=/root/bin/plugin-enable.sh

${enpl} local k8smon nodes
${enpl} local nginx

exit 0
