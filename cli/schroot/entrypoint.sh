#!/bin/sh
set -eu

doas install -v -m 0440 -o root -g root \
	./host/assets/jsbatch/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

doas install -v -d -m 0750 -o uws -g uws /home/uws

doas /usr/sbin/adduser uws ${SCHROOT_GROUP}
doas /usr/sbin/adduser uws docker

doas install -v -d -m 0750 -o root -g uws /etc/uws
doas ln -vsf /srv/uws/deploy/cli/schroot/etc /etc/uws/cli

doas install -v -d -m 0750 -o root -g uws /srv/deploy
doas ln -vsf /srv/uws/deploy/cli/schroot/builder /srv/deploy/uwspod

doas install -v -d /srv/docker/lib

doas rm -rf /run/uwscli
doas install -v -d -m 0750 -o uws -g uwscli /run/uwscli
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/nq
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/build
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/logs

doas rm -rf /usr/local/bin
doas ln -vsf /srv/uws/deploy/cli/schroot/bin /usr/local/bin

PATH=/srv/home/uwscli/bin:${PATH}
exec /bin/bash -i
