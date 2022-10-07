#!/bin/sh
set -eu

profile=${1:?'uwscli profile?'}

UWSCLI_PROFILE="${profile}"
export UWSCLI_PROFILE

#
# host setup
#
echo "uwscli-${profile}" >/etc/hostname

#
# rsyslogd
#
install -v -m 0644 /srv/home/uwscli/etc/rsyslog.conf /etc/
install -v -m 0644 /srv/home/uwscli/etc/rsyslog.d/uws.conf /etc/rsyslog.d/

ln -svf /etc/monit/conf-available/rsyslog /etc/monit/conf-enabled

/etc/init.d/rsyslog start

#
# msmtp
#
/srv/home/uwscli/sbin/msmtp_init.sh

#
# docker
#
echo 'export DOCKER_RAMDISK=true' >/etc/default/docker
ln -svf /srv/home/uwscli/etc/monit/conf/docker /etc/monit/conf-enabled
/etc/init.d/docker start

#
# cron
#
/srv/home/uwscli/sbin/cron_init.sh

#
# sshd
#
/srv/home/uwscli/sbin/sshd_init.sh

#
# make setup
#
uwsrun='sudo -n -u uws'
${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

#
# monit
#
exec /srv/home/uwscli/sbin/monit.sh
