#!/bin/sh
set -eu

umask 0027

# sudoers

install -v -m 0640 -o root -g root \
	~uwscli/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

# utils access

chmod -v 0750 ~uwscli
chown -v uwscli:uwscli ~uwscli

chmod -v 0750 ~uwscli/etc
chown -vR root:uwscli ~uwscli/etc

chmod -v 0750 ~uwscli/lib
chown -vR root:uwscli ~uwscli/lib

chmod -v 0750 ~uwscli/vendor
chown -vR root:uwscli ~uwscli/vendor

chmod -v 0550 ~uwscli/bin/*
chmod -v 0750 ~uwscli/bin
chown -vR root:uwscli ~uwscli/bin

adduser uws uwscli

# operator utils

addgroup uwsops || true

chown -v root:uwsops ~uwscli/bin/app-deploy
chown -v root:uwsops ~uwscli/bin/app-rollin
chown -v root:uwsops ~uwscli/bin/app-scale

# internal utils

chown -v uwscli:root ~uwscli/bin/app-autobuild

# python compile lib and vendor

umask 0022

rm -vrf ~uwscli/lib/__pycache__

python3 -m compileall ~uwscli/lib

chown -R root:uwscli ~uwscli/lib/__pycache__

find ~uwscli/vendor/ -type d -name __pycache__ -print0 |
	xargs -0 rm -rf

python3 -m compileall ~uwscli/vendor

find ~uwscli/vendor/ -type d -name __pycache__ -print0 |
	xargs -0 chown -R root:uwscli

exit 0
