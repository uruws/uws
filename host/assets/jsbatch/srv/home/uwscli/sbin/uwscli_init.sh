#!/bin/sh
set -eu

profile=${1:?'uwscli profile?'}

UWSCLI_PROFILE="${profile}"
export UWSCLI_PROFILE

#
# hosts setup
#
#~ echo "127.0.0.1 uwscli-${profile} localhost" >/etc/hosts.new
#~ grep -F ip6 /etc/hosts >>/etc/hosts.new
#~ cat /etc/hosts.new >/etc/hosts
#~ rm -vf /etc/hosts.new
echo "127.10.0.1 uwscli-${profile}" >>/etc/hosts

#
# rsyslogd
#
install -v -m 0644 /srv/home/uwscli/etc/rsyslog.conf /etc/
install -v -m 0644 /srv/home/uwscli/etc/rsyslog.d/uws.conf /etc/rsyslog.d/

ln -svf /etc/monit/conf-available/rsyslog /etc/monit/conf-enabled

/etc/init.d/rsyslog start
sleep 1

#
# init services
#

install -v -d -o root -g root  -m 0755 /usr/local/ca

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
