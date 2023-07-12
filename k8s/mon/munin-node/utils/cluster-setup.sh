#!/bin/sh
set -eu

# compile all

python3 -m compileall /srv/munin/plugins/*.py

# enable munin-node parallel plugins

install -v -m 0755 /srv/munin/plugins/mnppl.py /usr/local/bin/mnppl

enpl=/root/bin/plugin-enable.sh

${enpl} local mnppl

# mnppl plugins to run

install -v -m 0755 /srv/munin/plugins/nodes.py       /usr/local/bin/nodes.mnppl
#install -v -m 0755 /srv/munin/plugins/nginx.py       /usr/local/bin/nginx.mnppl
install -v -m 0755 /srv/munin/plugins/deployments.py /usr/local/bin/deployments.mnppl
install -v -m 0755 /srv/munin/plugins/pods.py        /usr/local/bin/pods.mnppl
#install -v -m 0755 /srv/munin/plugins/k8s.py         /usr/local/bin/k8s.mnppl
install -v -m 0755 /srv/munin/plugins/munin.py       /usr/local/bin/munin.mnppl

# plugins config

cat <<EOF >/etc/munin/plugin-conf.d/uws
[mnppl]
user uws
group uws
EOF

exit 0
