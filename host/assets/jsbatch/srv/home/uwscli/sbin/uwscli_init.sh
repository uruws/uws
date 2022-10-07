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
# init services
#
/srv/home/uwscli/sbin/msmtp_init.sh
/srv/home/uwscli/sbin/docker_init.sh
/srv/home/uwscli/sbin/cron_init.sh
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
