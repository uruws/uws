#!/bin/sh
set -eu

# rsyslogd

install -v /srv/home/uwscli/etc/rsyslog.conf /etc/
install -v /srv/home/uwscli/etc/rsyslog.d/uws.conf /etc/rsyslog.d/

# monit workaround
touch /var/log/syslog
chown -v root:adm /var/log/syslog
chmod -v 0640     /var/log/syslog

/etc/init.d/rsyslog start
sleep 1

# docker

echo 'export DOCKER_RAMDISK=true' >/etc/default/docker

/etc/init.d/docker start
sleep 1

# sshd

# monit workaround
touch /etc/ssh/ssh_host_dsa_key
chown -v root:root /etc/ssh/ssh_host_dsa_key
chmod -v 0600      /etc/ssh/ssh_host_dsa_key

/srv/home/uwscli/sbin/sshd_init.sh
sleep 1

# make setup

uwsrun='sudo -n -u uws'

${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

# monit

/srv/home/uwscli/sbin/monit.sh
