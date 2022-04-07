#!/bin/sh
set -eu

umask 0027

# docker setup

echo 'export DOCKER_RAMDISK=true' >/etc/default/docker

# home dir

install -v -d -o root -g root -m 0751 /srv/home

# internal groups

groupadd -g 1500 uwsadm || true
groupadd -g 1600 uwsops || true

# internal users

# uws
groupadd -g 3000 uws || true
useradd -d /srv/home/uws -m -c 'uws' -s /bin/bash -g 3000 -u 3000 uws || true
chmod -v 0750 /srv/home/uws

adduser uws docker

# uwscli
groupadd -g 3100 uwscli || true
useradd -d /srv/home/uwscli -M -c 'uwscli' -s /bin/bash -g 3100 -u 3100 uwscli || true
chmod -v 0750 /srv/home/uwscli

adduser uws uwscli

# sudoers

install -v -C -m 0640 -o root -g root \
	~uwscli/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

# run dirs

install -v -d -o uws -g uwscli -m 0750 /run/uwscli
install -v -d -o uws -g uwscli -m 0770 /run/uwscli/nq
install -v -d -o uws -g uwscli -m 0770 /run/uwscli/build
#install -v -d -o uws -g uwscli -m 0770 /run/uwscli/logs

# utils access

install -v -d -m 0750 -o root -g uwscli ~uwscli
install -v -d -m 0750 -o root -g uwscli ~uwscli/etc
install -v -d -m 0750 -o root -g uwscli ~uwscli/lib
install -v -d -m 0750 -o root -g uwscli ~uwscli/vendor
install -v -d -m 0750 -o root -g uwscli ~uwscli/bin
install -v -d -m 0750 -o root -g root   ~uwscli/sbin

chown -vR root:uwscli ~uwscli/etc/bash_profile

chown -vR root:uwscli ~uwscli/bin
chmod -v 0550 ~uwscli/bin/*

chown -vR root:root ~uwscli/sbin
chmod -v 0550 ~uwscli/sbin/*.*

chown -vR root:uwscli /srv/uws/deploy

# operator utils

chown -v root:uwsops ~uwscli/bin/app-deploy
chown -v root:uwsops ~uwscli/bin/app-rollin
chown -v root:uwsops ~uwscli/bin/app-scale

# internal utils

chown -v uwscli:root ~uwscli/bin/app-autobuild

# python compile lib and vendor

umask 0022

rm -rf ~uwscli/lib/__pycache__

python3 -m compileall ~uwscli/lib

chown -R root:uwscli ~uwscli/lib

find ~uwscli/vendor/ -type d -name __pycache__ -print0 |
	xargs -0 rm -rf

python3 -m compileall ~uwscli/vendor

chown -R root:uwscli ~uwscli/vendor

# uwscli user

install -v -C -o root -g uwscli -m 0640 \
	~uwscli/etc/user.bash_profile ~uwscli/.bash_profile

adduser uwscli uwsadm
adduser uwscli uwsops

exit 0
