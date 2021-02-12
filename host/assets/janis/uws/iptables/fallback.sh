#!/bin/sh
set -eu
srcd=/uws/iptables
dstd=/etc/iptables
cat ${srcd}/rules.v4 >${dstd}/rules.v4
cat ${srcd}/rules.v6 >${dstd}/rules.v6
systemctl reload netfilter-persistent || /etc/init.d/netfilter-persistent flush
exit 0
