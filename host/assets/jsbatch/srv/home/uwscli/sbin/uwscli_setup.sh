#!/bin/sh
set -eu

umask 0027

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

# Allow uws user docker access.
adduser uws docker

# Make uws user an admin. Needed for autobuild deploys.
adduser uws uwsadm

# uws logs dir
install -v -d -o uws -g uws -m 0750 ~uws/logs

# uws SSH setup
install -v -d -o uws -g uws -m 0750 ~uws/.ssh
install -v -C -o uws -g uws -m 0400 /usr/local/etc/ssh/id_ed25519     ~uws/.ssh/
install -v -C -o uws -g uws -m 0440 /usr/local/etc/ssh/id_ed25519.pub ~uws/.ssh/
install -v -C -o uws -g uws -m 0440 /usr/local/etc/ssh/config         ~uws/.ssh/

# uwscli
groupadd -g 3100 uwscli || true
useradd -d /srv/home/uwscli -M -c 'uwscli' -s /bin/bash -g 3100 -u 3100 uwscli || true
chmod -v 0750 /srv/home/uwscli

adduser uws    uwscli
adduser uwscli uws

install -v -C -o root -g uwscli -m 0640 \
	~uwscli/etc/user.bash_profile ~uwscli/.bash_profile

adduser uwscli uwsadm
adduser uwscli uwsops

# sudoers

install -v -C -m 0640 -o root -g root \
	~uwscli/etc/sudoers.d/99-uws \
	/etc/sudoers.d/99-uws

install -v -C -m 0640 -o root -g root \
	~uwscli/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

# run dirs

install -v -d -o uws  -g uwscli -m 0750 /run/uwscli
install -v -d -o uws  -g uwscli -m 0770 /run/uwscli/nq
install -v -d -o uws  -g uwscli -m 0770 /run/uwscli/build

install -v -d -o uws -g uws -m 0750 /run/uwscli/auth

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

chown -R root:uws /srv/uws/deploy
chown -vR uws:uws /srv/uws/deploy/secret/eks/kube/cluster

# operator utils

chown -v root:uwsops ~uwscli/bin/app-deploy
chown -v root:uwsops ~uwscli/bin/app-restart
chown -v root:uwsops ~uwscli/bin/app-rollin
chown -v root:uwsops ~uwscli/bin/app-scale

# internal utils

chown -v uwscli:uws ~uwscli/bin/app-autobuild

# api auth ssh

install -v -d -o uws -g uws -m 0750 /run/uwscli/auth/ssh
install -v -C -o uws -g uws -m 0400 /usr/local/etc/ssh/id_ed25519     /run/uwscli/auth/ssh/
install -v -C -o uws -g uws -m 0440 /usr/local/etc/ssh/id_ed25519.pub /run/uwscli/auth/ssh/
install -v -C -o uws -g uws -m 0440 /usr/local/etc/ssh/config         /run/uwscli/auth/ssh/

# python compile lib and vendor

umask 0022

rm -rf /etc/uws/cli/__pycache__
rm -rf ~uwscli/lib/__pycache__

python3 -m compileall ~uwscli/lib

chown -R root:uwscli ~uwscli/lib

find ~uwscli/vendor/ -type d -name __pycache__ -print0 |
	xargs -0 rm -rf

python3 -m compileall ~uwscli/vendor

chown -R root:uwscli ~uwscli/vendor

if test -d /etc/uws/cli/__pycache__; then
	chown -R root:uwscli /etc/uws/cli/__pycache__
fi

exit 0
