#!/bin/sh
set -eu

uwsrun='sudo -n -u uws'

# docker

echo 'export DOCKER_RAMDISK=true' >/etc/default/docker

/etc/init.d/docker start
sleep 1

# sshd

/srv/home/uwscli/sbin/sshd_init.sh
sleep 1

# make setup

${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

# monit

exec /srv/home/uwscli/sbin/monit.sh
