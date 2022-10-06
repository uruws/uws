#!/bin/sh
set -eu

#
# rsyslogd
#

install -v -m 0644 /srv/home/uwscli/etc/rsyslog.conf /etc/
install -v -m 0644 /srv/home/uwscli/etc/rsyslog.d/uws.conf /etc/rsyslog.d/

/etc/init.d/rsyslog start
sleep 1

#
# docker
#
echo 'export DOCKER_RAMDISK=true' >/etc/default/docker
/etc/init.d/docker start
sleep 1

#
# sshd
#
/srv/home/uwscli/sbin/sshd_init.sh
sleep 1

#
# make setup
#
uwsrun='sudo -n -u uws'
${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

#
# monit
#
exec /srv/home/uwscli/sbin/monit.sh
