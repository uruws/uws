#!/bin/sh
set -eu

# sudo

doas install -v -m 0440 -o root -g root \
	./host/assets/jsbatch/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

doas install -v -d -m 0750 -o uws -g uws /home/uws

# uws user

doas /usr/sbin/adduser uws ${SCHROOT_GROUP}
doas /usr/sbin/adduser uws docker

# local conf

doas install -v -d -m 0750 -o root -g uws /etc/uws
doas ln -vsf /srv/uws/deploy/cli/schroot/etc /etc/uws/cli

# podtest builder

doas install -v -d -m 0750 -o root -g uws /srv/deploy
doas ln -vsf /srv/uws/deploy/cli/schroot/builder /srv/deploy/uwspod

doas install -v -d /srv/docker/lib

# run dirs

doas rm -rf /run/uwscli
doas install -v -d -m 0750 -o uws -g uwscli /run/uwscli
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/nq
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/build
doas install -v -d -m 0770 -o uws -g uwscli /run/uwscli/logs

# fake local commands

doas rm -rf /usr/local/bin
doas ln -vsf /srv/uws/deploy/cli/schroot/bin /usr/local/bin

# aws config

doas install -v -d -m 0750 -o ${SCHROOT_USER} -g ${SCHROOT_GROUP} ${HOME}
doas ln -vsf /srv/uws/deploy/secret/aws ${HOME}/.aws

# login

PATH=/srv/home/uwscli/bin:${PATH}
exec /bin/bash -i
