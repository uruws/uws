#!/bin/sh
set -eu

# docker

echo 'export DOCKER_RAMDISK=true' >/etc/default/docker

/etc/init.d/docker start
sleep 1

# sshd

/srv/home/uwscli/sbin/sshd_init.sh
sleep 1

# make setup

uwsrun='sudo -n -u uws'

${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

# monit

/srv/home/uwscli/sbin/monit.sh

# rsyslogd

install -v /srv/home/uwscli/etc/rsyslog.conf /etc/
install -v /srv/home/uwscli/etc/rsyslog.d/uws.conf /etc/rsyslog.d/

exec /usr/sbin/rsyslogd -n
