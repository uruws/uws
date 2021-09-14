#!/bin/sh
set -eu

python3 -m compileall /srv/munin/plugins/*.py

install -v -m 0755 /srv/munin/plugins/nodes.py /usr/local/bin/nodes
install -v -m 0755 /srv/munin/plugins/nginx.py /usr/local/bin/nginx

enpl=/root/bin/plugin-enable.sh

${enpl} local nodes
${enpl} local nginx

exit 0
