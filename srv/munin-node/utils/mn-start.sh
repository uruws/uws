#!/bin/sh
set -eu
setupfn=/srv/etc/munin-node/setup.sh
if test -x ${setupfn}; then
	${setupfn}
fi
# do prepare
/etc/init.d/munin-node start
/etc/init.d/munin-node stop
# log to stderr
rm -vf /var/log/munin/munin-node.log
ln -svf /dev/stderr /var/log/munin/munin-node.log
# run munin-node
exec /usr/sbin/munin-node --foreground
