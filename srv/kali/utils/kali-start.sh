#!/bin/sh
set -eu

chpasswd </root/etc/passwd

rm -vf /var/log/xrdp-sesman.log
ln -sv /dev/stdout /var/log/xrdp-sesman.log
xrdp-sesman -n &

sleep 2

rm -vf /var/log/xrdp.log
ln -sv /dev/stdout /var/log/xrdp.log
exec xrdp -n -p 3327
