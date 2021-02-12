#!/bin/sh
set -eu
rm -fr /mnt/munin/contrib
mkdir -vp /mnt/munin/contrib
tar -C /uws/munin/contrib -cf - . | tar -C /mnt/munin/contrib -xf -
rm -vf /mnt/munin/plugin-*.sh
install -m 0755 -o root -g root /root/bin/plugin-*.sh /mnt/munin
exit 0
