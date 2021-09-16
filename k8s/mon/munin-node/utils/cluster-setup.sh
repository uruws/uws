#!/bin/sh
set -eu

python3 -m compileall /srv/munin/plugins/*.py

install -v -m 0755 /srv/munin/plugins/nodes.py /usr/local/bin/nodes
install -v -m 0755 /srv/munin/plugins/nginx.py /usr/local/bin/nginx
install -v -m 0755 /srv/munin/plugins/deployments.py /usr/local/bin/deployments
install -v -m 0755 /srv/munin/plugins/pods.py /usr/local/bin/pods

enpl=/root/bin/plugin-enable.sh

${enpl} local nodes
${enpl} local nginx
${enpl} local deployments
${enpl} local pods

exit 0
