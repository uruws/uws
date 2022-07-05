#!/bin/sh
set -eu

python3 -m compileall /srv/munin/plugins/*.py

install -v -m 0755 /srv/munin/plugins/nodes.py       /usr/local/bin/nodes
install -v -m 0755 /srv/munin/plugins/nginx.py       /usr/local/bin/nginx
install -v -m 0755 /srv/munin/plugins/deployments.py /usr/local/bin/deployments
install -v -m 0755 /srv/munin/plugins/pods.py        /usr/local/bin/pods
install -v -m 0755 /srv/munin/plugins/k8s.py         /usr/local/bin/k8s
install -v -m 0755 /srv/munin/plugins/munin.py       /usr/local/bin/munin

enpl=/root/bin/plugin-enable.sh

${enpl} local nodes
${enpl} local nginx
${enpl} local deployments
${enpl} local pods
${enpl} local k8s
${enpl} local munin

cat <<EOF >/etc/munin/plugin-conf.d/uws
[munin]
user uws
group uws
EOF

exit 0
