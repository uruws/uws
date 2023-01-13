#!/bin/sh
set -eu

# setup plugins
setupfn=/srv/etc/munin-node/setup.sh
if test -s ${setupfn}; then
	/bin/sh -eu ${setupfn}
fi

# configure
if test -s /srv/etc/munin-node/munin-node.conf; then
	cp -v /srv/etc/munin-node/munin-node.conf /etc/munin
fi
if test -d /srv/etc/munin-node/plugin-conf.d; then
	cp -vr /srv/etc/munin-node/plugin-conf.d /etc/munin
fi
if test -d /srv/etc/sec/munin-node/plugin-conf.d; then
	cp -vr /srv/etc/sec/munin-node/plugin-conf.d /etc/munin
fi

# from /etc/init.d/munin-node
mkdir -p /run/munin /var/log/munin
chown munin:root /run/munin
chown munin:adm /var/log/munin
chmod 0755 /run/munin
chmod 0755 /var/log/munin

# do prepare
#~ /etc/init.d/munin-node start
#~ /etc/init.d/munin-node stop

# log to stderr
rm -vf /var/log/munin/munin-node.log
ln -svf /dev/stderr /var/log/munin/munin-node.log

# run munin-node
exec /usr/sbin/munin-node --foreground
